using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows;
using System.Windows.Input;
using Microsoft.Data.Sqlite;
using TestManager.Helpers; // Здесь лежит твой RelayCommand
using TestManager.Models;

namespace TestManager.ViewModels
{
    public class HistoryViewModel : INotifyPropertyChanged
    {
        public ObservableCollection<TestRecord> TestHistory { get; } = new ObservableCollection<TestRecord>();

        public ICommand RefreshCommand { get; }

        public HistoryViewModel()
        {
            RefreshCommand = new RelayCommand(_ => LoadHistoryFromDb());

            LoadHistoryFromDb();
        }

        private void LoadHistoryFromDb()
        {
            string dbPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "scripts", "test_results.db");

            if (!File.Exists(dbPath)) return;

            Application.Current.Dispatcher.Invoke(() => TestHistory.Clear());

            try
            {
                SQLitePCL.Batteries.Init();
                using (var connection = new SqliteConnection($"Data Source={dbPath}"))
                {
                    connection.Open();
                    var command = connection.CreateCommand();
                    // Лимит в 500 записей, чтобы интерфейс не завис, если тестов будут тысячи
                    command.CommandText = "SELECT id, timestamp, test_source, command, target_value, status, output FROM test_results ORDER BY id DESC LIMIT 500";

                    using (var reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            var record = new TestRecord
                            {
                                Id = reader.GetInt32(0),
                                Timestamp = reader.GetString(1),
                                Source = reader.GetString(2),
                                Command = reader.GetString(3),
                                TargetValue = reader.IsDBNull(4) ? "N/A" : reader.GetString(4),
                                Status = reader.GetString(5),
                                Output = reader.GetString(6)
                            };

                            Application.Current.Dispatcher.Invoke(() => TestHistory.Add(record));
                        }
                    }
                }
                // Обновляем счетчик элементов в интерфейсе
                OnPropertyChanged(nameof(TestHistory));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки БД:\n{ex.Message}\n\nПуть к файлу: {dbPath}",
                                "Ошибка БД", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}