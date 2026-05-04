using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Input;
using Renci.SshNet;
using TestManager.Helpers;
using TestManager.Models;
using TestManager.Services;

namespace TestManager.ViewModels
{
    public class ConnectionViewModel : INotifyPropertyChanged
    {
        private readonly INavigationService _navigationService;

        private string _ip;
        private string _role;
        private string _password;
        private string _status;

        public string IP
        {
            get => _ip;
            set { _ip = value; OnPropertyChanged(); RaiseCanExecuteChanged(); }
        }

        public string Role
        {
            get => _role;
            set { _role = value; OnPropertyChanged(); }
        }

        public string Password
        {
            get => _password;
            set { _password = value; OnPropertyChanged(); RaiseCanExecuteChanged(); }
        }

        public string Status
        {
            get => _status;
            set { _status = value; OnPropertyChanged(); }
        }

        public ICommand ConnectCommand { get; }

        public ConnectionViewModel(INavigationService navigationService)
        {
            _navigationService = navigationService;
            ConnectCommand = new RelayCommand(_ => Connect(), _ => CanConnect());
        }

        private bool CanConnect()
        {
            return !string.IsNullOrWhiteSpace(IP)
                && !string.IsNullOrWhiteSpace(Password);
        }

        private async void Connect()
        {
            Status = "Connecting...";

            try
            {
                SwitchInfo switchInfo = null;

                await Task.Run(() =>
                {
                    using (var client = new SshClient(IP, Role ?? "admin", Password))
                    {
                        client.Connect();
                        if (!client.IsConnected)
                            throw new Exception("Connection Failed");

                        using (var stream = client.CreateShellStream("xterm", 80, 24, 800, 600, 1024))
                        {
                            Thread.Sleep(500);
                            if (stream.DataAvailable) stream.Read();

                            stream.WriteLine("system switch show");

                            string output = "";
                            int timeoutMs = 5000;
                            int delayMs = 150;
                            int elapsed = 0;

                            while (elapsed < timeoutMs)
                            {
                                if (stream.DataAvailable)
                                {
                                    output += stream.Read();

                                    if (output.Contains("#") || output.Contains(">") || output.Contains("MAC Address"))
                                    {
                                        Thread.Sleep(100);
                                        if (stream.DataAvailable) output += stream.Read();
                                        break;
                                    }
                                }

                                Thread.Sleep(delayMs);
                                elapsed += delayMs;
                            }

                            if (string.IsNullOrWhiteSpace(output))
                                throw new Exception("Timeout: No response from switch.");

                            var parser = new SwitchInfoParser();
                            switchInfo = parser.Parse(output);
                        }

                        switchInfo.Ip = IP;
                        switchInfo.Username = Role ?? "admin";
                        switchInfo.Password = Password; // Сохраняем введенный пароль
                        switchInfo.IsConnected = true;
                    }
                });

                _navigationService.NavigateToStatusView(switchInfo);
            }
            catch (Exception ex)
            {
                Status = $"Error: {ex.Message}";
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string p = null)
            => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(p));

        private void RaiseCanExecuteChanged()
            => (ConnectCommand as RelayCommand)?.RaiseCanExecuteChanged();
    }
}