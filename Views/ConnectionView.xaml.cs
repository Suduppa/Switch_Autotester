using System.Windows;
using TestManager.Services;
using TestManager.ViewModels;

namespace TestManager.Views
{
    public partial class ConnectionView : Window
    {
        public ConnectionView()
        {
            InitializeComponent();
            DataContext = new ConnectionViewModel(new NavigationService());
        }
    }
}
