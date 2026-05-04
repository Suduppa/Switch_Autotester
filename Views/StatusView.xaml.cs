using System.Windows;
using TestManager.Models;
using TestManager.ViewModels;

namespace TestManager.Views
{
    public partial class StatusView : Window
    {
        public StatusView(SwitchInfo info)
        {
            InitializeComponent();
            DataContext = new StatusViewModel(info);
        }
    }
}