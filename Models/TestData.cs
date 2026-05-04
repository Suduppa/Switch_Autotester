using System.Collections.Generic;

namespace TestManager.Models
{
    public class TestData
    {
        public List<string> str_valid { get; set; } = new List<string>();
        public List<string> str_invalid { get; set; } = new List<string>();
        public List<string> ips_valid { get; set; } = new List<string>();
        public List<string> ips_invalid { get; set; } = new List<string>();
        public List<string> time_valid { get; set; } = new List<string>();
        public List<string> time_invalid { get; set; } = new List<string>();

        public bool UseDelayedStart { get; set; } = false;
        public string StartTime { get; set; } = "00:00";
        public int RunCount { get; set; } = 1;
    }
}