using TestManager.Models;

namespace TestManager.ViewModels
{
    public class InfoViewModel
    {
        public SwitchInfo Switch { get; }

        public InfoViewModel(SwitchInfo info)
        {
            Switch = info;
        }
    }
}
