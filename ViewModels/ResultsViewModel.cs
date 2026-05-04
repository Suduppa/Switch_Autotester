using System;
using System.ComponentModel;
using System.Data;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using ExcelDataReader;
using TestManager.Helpers;

namespace TestManager.ViewModels
{
    public class ResultsViewModel : INotifyPropertyChanged
    {
        private DataTableCollection _sheets;
        public DataTableCollection Sheets
        {
            get => _sheets;
            set { _sheets = value; OnPropertyChanged(); }
        }

        public ICommand LoadReportCommand { get; }

        public ResultsViewModel()
        {
            LoadReportCommand = new RelayCommand(_ => LoadExcelReport());
        }

        public void LoadExcelReport()
        {
            string filePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "scripts", "test_results.xlsx");
            if (!File.Exists(filePath))
            {
                System.Diagnostics.Debug.WriteLine($"[Results] Файл отчета не найден по пути: {filePath}"); return;
            } // Если тесты еще не запускались, файла нет

            try
            {
                System.Text.Encoding.RegisterProvider(System.Text.CodePagesEncodingProvider.Instance);

                // Открываем файл. FileShare.ReadWrite позволяет читать его, даже если он открыт в самом Excel
                using (var stream = File.Open(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    using (var reader = ExcelReaderFactory.CreateReader(stream))
                    {
                        var result = reader.AsDataSet(new ExcelDataSetConfiguration()
                        {
                            ConfigureDataTable = (_) => new ExcelDataTableConfiguration() { UseHeaderRow = true }
                        });

                        Sheets = result.Tables;
                    }
                }
            }
            catch (Exception)
            {
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string n = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(n));
    }
}