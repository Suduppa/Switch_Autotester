using System.Text.RegularExpressions;
using TestManager.Models;

namespace TestManager.Services
{
    public class SwitchInfoParser
    {
        public SwitchInfo Parse(string sshOutput)
        {
            var info = new SwitchInfo();

            info.Model = Extract(sshOutput, "Model");
            info.FirmwareVersion = Extract(sshOutput, "Firmware Version");
            info.HostName = Extract(sshOutput, "Host name");
            info.SystemTime = Extract(sshOutput, "System Time");
            info.MAC = Extract(sshOutput, "MAC Address");


            return info;
        }

        //public PortInfo Parse(string sshOutput) {}
        private string Extract(string text, string key)
        {
            var regex = new Regex(
                key + @"\s*:\s*(.+)",
                RegexOptions.IgnoreCase | RegexOptions.Multiline);

            var match = regex.Match(text);
            return match.Success
                ? match.Groups[1].Value.Trim()
                : string.Empty;
        }
    }
}
