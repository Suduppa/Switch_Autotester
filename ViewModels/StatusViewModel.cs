using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using TestManager.Helpers;
using TestManager.Models;

namespace TestManager.ViewModels
{
    public class StatusViewModel : INotifyPropertyChanged
    {
        public SwitchInfo Switch { get; }

        private object _currentView;
        public object CurrentView { get => _currentView; set { _currentView = value; OnPropertyChanged(); } }

        private string _selectedMenu;
        public string SelectedMenu { get => _selectedMenu; set { _selectedMenu = value; OnPropertyChanged(); } }

        private readonly LogsViewModel _sharedLogsViewModel;
        private readonly ResultsViewModel _sharedResultsViewModel;

        public ICommand ShowInfoCommand { get; }
        public ICommand ShowParametersCommand { get; }
        public ICommand ShowTestsCommand { get; }
        public ICommand ShowResultsCommand { get; }
        public ICommand ShowLogsCommand { get; }
        public ICommand ShowConfigCommand { get; }

        public StatusViewModel(SwitchInfo info)
        {
            Switch = info;
            _sharedLogsViewModel = new LogsViewModel();
            _sharedResultsViewModel = new ResultsViewModel();

            ShowInfoCommand = new RelayCommand(_ => ShowInfo());
            ShowParametersCommand = new RelayCommand(_ => ShowParameters());
            ShowTestsCommand = new RelayCommand(_ => ShowTests());
            ShowResultsCommand = new RelayCommand(_ => ShowResults());
            ShowLogsCommand = new RelayCommand(_ => ShowLogs());
            ShowConfigCommand = new RelayCommand(_ => ShowConfig());

            ShowInfo();
            // Внутри конструктора StatusViewModel()
            _historyVM = new HistoryViewModel(); // Создаем экземпляр

            ShowHistoryCommand = new RelayCommand(_ =>
            {
                CurrentView = _historyVM;
                SelectedMenu = "History"; // Чтобы кнопочка расширилась
            });
        }

        private void ShowInfo() { SelectedMenu = "Info"; CurrentView = new InfoViewModel(Switch); }
        private void ShowParameters() { SelectedMenu = "Parameters"; CurrentView = new ParametersViewModel(); }

        private void ShowTests()
        {
            SelectedMenu = "Tests";
            CurrentView = new TestsViewModel(_sharedLogsViewModel, Switch);
        }

        private void ShowLogs()
        {
            SelectedMenu = "Logs";
            CurrentView = _sharedLogsViewModel; // вывод логов
        }

        private void ShowResults()
        {
            SelectedMenu = "Results";
            _sharedResultsViewModel.LoadExcelReport();
            CurrentView = _sharedResultsViewModel;
        }

        private void ShowConfig() { SelectedMenu = "Config"; CurrentView = new ConfigViewModel(); }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string n = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(n));

        private HistoryViewModel _historyVM;
        public ICommand ShowHistoryCommand { get; }


    }
}