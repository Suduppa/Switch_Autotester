using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TestManager.Models;

namespace TestManager.ViewModels
{
    public class LogsViewModel
    {
        public ObservableCollection<LogMessage> Logs { get; } = new ObservableCollection<LogMessage>();

        public void Clear()
        {
            Logs.Clear();
        }

        public void AddLog(string text, string color = "#FF091B41")
        {
            Logs.Add(new LogMessage { Text = text, Color = color });
        }
    }
}
