using System.Collections.Specialized;
using System.Windows;
using System.Windows.Controls;

namespace TestManager.Helpers
{
    public static class AutoScrollBehavior
    {
        public static readonly DependencyProperty AutoScrollProperty =
            DependencyProperty.RegisterAttached(
                "AutoScroll",
                typeof(bool),
                typeof(AutoScrollBehavior),
                new PropertyMetadata(false, AutoScrollPropertyChanged));

        public static bool GetAutoScroll(DependencyObject obj) => (bool)obj.GetValue(AutoScrollProperty);
        public static void SetAutoScroll(DependencyObject obj, bool value) => obj.SetValue(AutoScrollProperty, value);

        private static void AutoScrollPropertyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            if (d is ListBox listBox)
            {
                // Отписываемся от событий жизненного цикла
                listBox.Loaded -= ListBox_Loaded;
                listBox.Unloaded -= ListBox_Unloaded;

                if ((bool)e.NewValue)
                {
                    // Подписываемся заново
                    listBox.Loaded += ListBox_Loaded;
                    listBox.Unloaded += ListBox_Unloaded;

                    // Если ListBox уже на экране, цепляем прокрутку сразу
                    if (listBox.IsLoaded)
                    {
                        Subscribe(listBox);
                    }
                }
                else
                {
                    Unsubscribe(listBox);
                }
            }
        }

        private static void ListBox_Loaded(object sender, RoutedEventArgs e) => Subscribe((ListBox)sender);
        private static void ListBox_Unloaded(object sender, RoutedEventArgs e) => Unsubscribe((ListBox)sender);

        private static void Subscribe(ListBox listBox)
        {
            if (listBox.Items is INotifyCollectionChanged collection)
            {
                // Создаем локальную функцию-обработчик
                NotifyCollectionChangedEventHandler handler = (s, e) =>
                {
                    if (e.Action == NotifyCollectionChangedAction.Add && e.NewItems != null)
                    {
                        Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            // Двойная проверка флага перед прокруткой
                            if (GetAutoScroll(listBox))
                            {
                                listBox.ScrollIntoView(e.NewItems[e.NewItems.Count - 1]);
                            }
                        });
                    }
                };

                // Сохраняем ссылку на обработчик в Tag, чтобы потом корректно отписаться (избегаем утечек памяти)
                listBox.Tag = handler;
                collection.CollectionChanged += handler;
            }
        }

        private static void Unsubscribe(ListBox listBox)
        {
            if (listBox.Items is INotifyCollectionChanged collection && listBox.Tag is NotifyCollectionChangedEventHandler handler)
            {
                collection.CollectionChanged -= handler;
                listBox.Tag = null;
            }
        }
    }
}