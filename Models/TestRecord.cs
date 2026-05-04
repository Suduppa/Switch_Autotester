namespace TestManager.Models
{
    public class TestRecord
    {
        public int Id { get; set; }
        public string Timestamp { get; set; }
        public string Source { get; set; }
        public string Command { get; set; }
        public string TargetValue { get; set; }
        public string Status { get; set; }
        public string Output { get; set; }
    }
}