using System;
using System.Windows;
using TestManager.Models;
using TestManager.Views;

namespace TestManager.Services
{
    public interface INavigationService
    {
        void NavigateToStatusView(SwitchInfo info);
    }

    public class NavigationService : INavigationService
    {
        public void NavigateToStatusView(SwitchInfo info)
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                var statusView = new StatusView(info);
                statusView.Show();

                foreach (Window w in Application.Current.Windows)
                {
                    if (w is ConnectionView)
                    {
                        w.Close();
                        break;
                    }
                }
            });
        }
    }
}