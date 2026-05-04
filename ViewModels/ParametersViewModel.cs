using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Windows.Input;
using TestManager.Helpers;
using TestManager.Models;

namespace TestManager.ViewModels
{
    public class ParametersViewModel : INotifyPropertyChanged
    {
        private readonly string _jsonFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "scripts", "test_data.json");
        private TestData _currentData = new TestData();

        public ObservableCollection<string> ValidValues { get; } = new ObservableCollection<string>();
        public ObservableCollection<string> InvalidValues { get; } = new ObservableCollection<string>();

        public bool UseDelayedStart
        {
            get => _currentData.UseDelayedStart;
            set { _currentData.UseDelayedStart = value; OnPropertyChanged(); SaveData(); }
        }

        public string StartTime
        {
            get => _currentData.StartTime;
            set { _currentData.StartTime = value; OnPropertyChanged(); SaveData(); }
        }

        public int RunCount
        {
            get => _currentData.RunCount;
            set { _currentData.RunCount = value; OnPropertyChanged(); SaveData(); }
        }

        private string _newValidValue;
        public string NewValidValue
        {
            get => _newValidValue;
            set
            {
                _newValidValue = value;
                OnPropertyChanged();
                (AddValidCommand as RelayCommand)?.RaiseCanExecuteChanged();
            }
        }

        private string _newInvalidValue;
        public string NewInvalidValue
        {
            get => _newInvalidValue;
            set
            {
                _newInvalidValue = value;
                OnPropertyChanged();
                (AddInvalidCommand as RelayCommand)?.RaiseCanExecuteChanged();
            }
        }

        public string SelectedValidValue { get; set; }
        public string SelectedInvalidValue { get; set; }

        public ICommand AddValidCommand { get; }
        public ICommand RemoveValidCommand { get; }
        public ICommand AddInvalidCommand { get; }
        public ICommand RemoveInvalidCommand { get; }

        public ParametersViewModel()
        {
            AddValidCommand = new RelayCommand(_ => AddValid(), _ => !string.IsNullOrWhiteSpace(NewValidValue)); //true);
            RemoveValidCommand = new RelayCommand(_ => RemoveValid());
            AddInvalidCommand = new RelayCommand(_ => AddInvalid(), _ => !string.IsNullOrWhiteSpace(NewInvalidValue));
            RemoveInvalidCommand = new RelayCommand(_ => RemoveInvalid());

            LoadData();
        }

        private void LoadData()
        {
            if (File.Exists(_jsonFilePath))
            {
                try
                {
                    string json = File.ReadAllText(_jsonFilePath);
                    _currentData = JsonSerializer.Deserialize<TestData>(json) ?? new TestData();
                }
                catch { _currentData = new TestData(); }
            }

            ValidValues.Clear();
            foreach (var item in _currentData.str_valid) ValidValues.Add(item);

            InvalidValues.Clear();
            foreach (var item in _currentData.str_invalid) InvalidValues.Add(item);

            OnPropertyChanged(nameof(UseDelayedStart));
            OnPropertyChanged(nameof(StartTime));
            OnPropertyChanged(nameof(RunCount));
        }

        private void SaveData()
        {
            _currentData.str_valid = ValidValues.ToList();
            _currentData.str_invalid = InvalidValues.ToList();

            var options = new JsonSerializerOptions { WriteIndented = true };
            File.WriteAllText(_jsonFilePath, JsonSerializer.Serialize(_currentData, options));
        }

        private void AddValid() { if (!ValidValues.Contains(NewValidValue)) { ValidValues.Add(NewValidValue); SaveData(); } NewValidValue = ""; }
        private void RemoveValid() { if (SelectedValidValue != null) { ValidValues.Remove(SelectedValidValue); SaveData(); } }
        private void AddInvalid() { if (!InvalidValues.Contains(NewInvalidValue)) { InvalidValues.Add(NewInvalidValue); SaveData(); } NewInvalidValue = ""; }
        private void RemoveInvalid() { if (SelectedInvalidValue != null) { InvalidValues.Remove(SelectedInvalidValue); SaveData(); } }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string n = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(n));
    }
}