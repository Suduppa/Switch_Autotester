using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using TestManager.Models;

namespace TestManager.ViewModels
{
    public class LogsViewModel : INotifyPropertyChanged
    {
        // Три отдельных списка для логов
        public ObservableCollection<LogMessage> SshLogs { get; } = new ObservableCollection<LogMessage>();
        public ObservableCollection<LogMessage> WebLogs { get; } = new ObservableCollection<LogMessage>();
        public ObservableCollection<LogMessage> SnmpLogs { get; } = new ObservableCollection<LogMessage>();

        // Состояние кнопки автопрокрутки (по умолчанию включена)
        private bool _autoScroll = true;
        public bool AutoScroll
        {
            get => _autoScroll;
            set { _autoScroll = value; OnPropertyChanged(); }
        }

        public void Clear()
        {
            // Очищаем все списки
            System.Windows.Application.Current.Dispatcher.Invoke(() => {
                SshLogs.Clear();
                WebLogs.Clear();
                SnmpLogs.Clear();
            });
        }

        public void AddLog(string protocol, string text, string color = "#FF091B41")
        {
            var msg = new LogMessage { Text = text, Color = color };

            // Распределяем по вкладкам
            if (protocol == "WEB") WebLogs.Add(msg);
            else if (protocol == "SNMP") SnmpLogs.Add(msg);
            else SshLogs.Add(msg); // Всё остальное (SSH и системные ошибки) кидаем в основу
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}