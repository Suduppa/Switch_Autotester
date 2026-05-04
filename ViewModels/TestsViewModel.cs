using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using TestManager.Helpers;
using TestManager.Models;
using System.IO;

namespace TestManager.ViewModels
{
    public class TestsViewModel : INotifyPropertyChanged
    {
        private readonly LogsViewModel _logsViewModel;
        private readonly SwitchInfo _switchInfo;
        private bool _isRunning;

        public ObservableCollection<TestItem> AvailableTests { get; } = new ObservableCollection<TestItem>();

        public bool IsRunning
        {
            get => _isRunning;
            set { _isRunning = value; OnPropertyChanged(); (StartTestsCommand as RelayCommand)?.RaiseCanExecuteChanged(); }
        }

        public ICommand StartTestsCommand { get; }

        public TestsViewModel(LogsViewModel logsViewModel, SwitchInfo switchInfo)
        {
            _logsViewModel = logsViewModel;
            _switchInfo = switchInfo;

            StartTestsCommand = new RelayCommand(_ => RunPythonTestsAsync(), _ => !IsRunning && AvailableTests.Any(t => t.IsSelected));

            LoadAvailableTests();
        }

        private async void LoadAvailableTests()
        {
            Application.Current.Dispatcher.Invoke(() => AvailableTests.Clear());

            await Task.Run(() =>
            {
                try
                {
                    string scriptsPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "scripts");

                    var startInfo = new ProcessStartInfo
                    {
                        FileName = "python",
                        Arguments = "run.py --list",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                        WorkingDirectory = scriptsPath,
                        StandardOutputEncoding = System.Text.Encoding.UTF8
                    };

                    using (Process process = new Process { StartInfo = startInfo })
                    {
                        process.Start();
                        string output = process.StandardOutput.ReadToEnd();
                        string error = process.StandardError.ReadToEnd();
                        process.WaitForExit();

                        if (!string.IsNullOrEmpty(error))
                        {
                            System.Diagnostics.Debug.WriteLine($"[Python Error]: {error}");
                        }

                        var lines = output.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);

                        foreach (var line in lines)
                        {
                            var testName = line.Trim();
                            if (string.IsNullOrEmpty(testName)) continue;

                            var testItem = new TestItem { Name = testName, IsSelected = false };

                            testItem.PropertyChanged += (s, e) =>
                            {
                                if (e.PropertyName == nameof(TestItem.IsSelected))
                                {
                                    Application.Current.Dispatcher.Invoke(() =>
                                    {
                                        (StartTestsCommand as RelayCommand)?.RaiseCanExecuteChanged();
                                    });
                                }
                            };

                            Application.Current.Dispatcher.Invoke(() => AvailableTests.Add(testItem));
                        }
                    }
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine($"[C# Error]: {ex.Message}");
                    Application.Current.Dispatcher.Invoke(() =>
                        _logsViewModel.AddLog($"Ошибка загрузки тестов: {ex.Message}", "Red"));
                }
            });
        }

        private async void RunPythonTestsAsync()
        {
            var selectedTests = AvailableTests.Where(t => t.IsSelected).Select(t => t.Name).ToList();
            if (!selectedTests.Any()) return;

            IsRunning = true;
            _logsViewModel.Clear();

            string scriptsPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "scripts");
            string arguments = $"run.py --ip {_switchInfo.Ip} --user {_switchInfo.Username} --psw \"{_switchInfo.Password}\" {string.Join(" ", selectedTests)}";

            await Task.Run(() =>
            {
                try
                {
                    var startInfo = new ProcessStartInfo
                    {
                        FileName = "python",
                        Arguments = arguments,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                        WorkingDirectory = scriptsPath, 
                        StandardOutputEncoding = System.Text.Encoding.UTF8,
                        StandardErrorEncoding = System.Text.Encoding.UTF8
                    };

                    using (Process process = new Process { StartInfo = startInfo })
                    {
                        process.OutputDataReceived += (s, e) => {
                            if (!string.IsNullOrEmpty(e.Data))
                            {
                                // Очистка от мусора colorama
                                string cleanText = System.Text.RegularExpressions.Regex.Replace(e.Data, @"\x1B\[[^@-~]*[@-~]", "");
                                Application.Current.Dispatcher.Invoke(() => AddColoredLog(cleanText));
                            }
                        };
                        process.ErrorDataReceived += (s, e) => {
                            if (!string.IsNullOrEmpty(e.Data))
                                Application.Current.Dispatcher.Invoke(() => AddColoredLog($"[Ошибка Python]: {e.Data}", "Red"));
                        };

                        startInfo.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8";

                        process.Start();
                        process.BeginOutputReadLine();
                        process.BeginErrorReadLine();
                        process.WaitForExit();
                    }
                }
                catch (Exception ex) { Application.Current.Dispatcher.Invoke(() => AddColoredLog($"Ошибка запуска: {ex.Message}", "Red")); }
                finally { Application.Current.Dispatcher.Invoke(() => IsRunning = false); }
            });
        }

        private void AddColoredLog(string text, string forceColor = null)
        {
            if (forceColor != null) { _logsViewModel.AddLog(text, forceColor); return; }

            string color = "#FF091B41"; // Базовый цвет (темно-синий)
            string lower = text.ToLower();

            if (lower.Contains("ошибка") || lower.Contains("error") || lower.Contains("failed") || lower.Contains("таймаут"))
                color = "#E53935"; // Красный
            else if (lower.Contains("успех") || lower.Contains("success") || text.Contains("✓"))
                color = "#43A047"; // Зеленый
            else if (lower.Contains("предупреждение") || lower.Contains("warning"))
                color = "#FB8C00"; // Оранжевый
            else if (text.StartsWith("→") || text.StartsWith(">>>"))
                color = "#00ACC1"; // Бирюзовый (информация о команде)
            else if (text.StartsWith("#"))
                color = "#8E24AA"; // Фиолетовый (комментарии)

            _logsViewModel.AddLog(text, color);
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}