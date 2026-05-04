//НЕ ИСПОЛЬЗУЕТСЯ

using System.Windows;
using System.Windows.Controls;

namespace TestManager.Helpers
{
    public static class PasswordHelper
    {
        public static readonly DependencyProperty AttachProperty =
            DependencyProperty.RegisterAttached(
                "Attach",
                typeof(bool),
                typeof(PasswordHelper),
                new PropertyMetadata(false, OnAttachChanged));

        public static readonly DependencyProperty PasswordProperty =
            DependencyProperty.RegisterAttached(
                "Password",
                typeof(string),
                typeof(PasswordHelper),
                new PropertyMetadata(string.Empty));

        public static bool GetAttach(DependencyObject obj)
            => (bool)obj.GetValue(AttachProperty);

        public static void SetAttach(DependencyObject obj, bool value)
            => obj.SetValue(AttachProperty, value);

        public static string GetPassword(DependencyObject obj)
            => (string)obj.GetValue(PasswordProperty);

        public static void SetPassword(DependencyObject obj, string value)
            => obj.SetValue(PasswordProperty, value);

        private static void OnAttachChanged(
            DependencyObject d,
            DependencyPropertyChangedEventArgs e)
        {
            if (d is PasswordBox passwordBox)
            {
                if ((bool)e.NewValue)
                {
                    passwordBox.PasswordChanged += PasswordChanged;
                }
                else
                {
                    passwordBox.PasswordChanged -= PasswordChanged;
                }
            }
        }

        private static void PasswordChanged(object sender, RoutedEventArgs e)
        {
            var passwordBox = (PasswordBox)sender;
            SetPassword(passwordBox, passwordBox.Password);
        }
    }
}
