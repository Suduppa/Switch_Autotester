/*using System.Windows;
using TestManager.Services;
using TestManager.ViewModels;
using TestManager.Views;

namespace TestManager
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            var navigationService = new NavigationService();
            var mainWindow = new ConnectionView
            {
                DataContext = new ConnectionViewModel(navigationService)
            };
            mainWindow.Show();
        }
    }
} */

using System.Windows;
using TestManager.Services;
using TestManager.ViewModels;
using TestManager.Views;

namespace TestManager
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            var navigationService = new NavigationService();
            var mainWindow = new ConnectionView();
            mainWindow.Show();
        }
    }
}
