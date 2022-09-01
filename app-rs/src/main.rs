#![no_std]
#![no_main]

extern crate panic_halt;

mod print;
mod timer;

use pac;
use riscv_rt::entry;
use timer::Timer;

use spacewire_rs::common::*;
use spacewire_rs::datalink::*;

struct AmaranthSpw {
    core: pac::SPW_NODE,
}

impl AmaranthSpw {
    pub fn new(core: pac::SPW_NODE) -> Self {
        AmaranthSpw { core }
    }

    fn link_error_clear(&self) {
        self.core
            .control
            .modify(|_, w| w.link_error_clear().bit(true));
    }
}

impl LowLevelAccess for AmaranthSpw {
    fn get_link_state(&self) -> Result<LinkState, DataLinkLayerError> {
        match self.core.status.read().link_state().bits() {
            0 => Ok(LinkState::ErrorReset),
            1 => Ok(LinkState::ErrorWait),
            2 => Ok(LinkState::Ready),
            3 => Ok(LinkState::Started),
            4 => Ok(LinkState::Connecting),
            5 => Ok(LinkState::Run),
            _ => Err(DataLinkLayerError::UnknownLinkState),
        }
    }

    fn set_link_start(&self, start: bool) -> Result<(), DataLinkLayerError> {
        self.core.control.modify(|_, w| w.link_start().bit(start));
        Ok(())
    }

    fn get_link_start(&self) -> Result<bool, DataLinkLayerError> {
        Ok(self.core.control.read().link_start().bit())
    }

    fn set_link_autostart(&self, start: bool) -> Result<(), DataLinkLayerError> {
        self.core.control.modify(|_, w| w.auto_start().bit(start));
        Ok(())
    }

    fn get_link_autostart(&self) -> Result<bool, DataLinkLayerError> {
        Ok(self.core.control.read().auto_start().bit())
    }

    fn port_reset(&self) -> Result<(), DataLinkLayerError> {
        Ok(self.core.control.modify(|_, w| w.soft_reset().bit(true)))
    }

    fn set_link_disabled(&self, disabled: bool) -> Result<(), DataLinkLayerError> {
        self.core
            .control
            .modify(|_, w| w.link_disabled().bit(disabled));
        Ok(())
    }

    fn get_link_disabled(&self) -> Result<bool, DataLinkLayerError> {
        Ok(self.core.control.read().link_disabled().bit())
    }

    fn get_link_error_flags(&self) -> Result<LinkError, DataLinkLayerError> {
        let bits = self.core.status.read().link_error_flags().bits();
        Ok(LinkError {
            disconnect: (bits >> 0) != 0,
            parity: (bits >> 1) != 0,
            escape: (bits >> 2) != 0,
            credit: (bits >> 3) != 0,
        })
    }

    fn get_link_credit(&self) -> Result<LinkCredit, DataLinkLayerError> {
        Ok(LinkCredit {
            tx: self.core.status.read().link_tx_credit().bits(),
            rx: self.core.status.read().link_rx_credit().bits(),
        })
    }
}

const SYSTEM_CLOCK_FREQUENCY: u32 = 54_000_000;

#[entry]
fn main() -> ! {
    let peripherals = pac::Peripherals::take().unwrap();

    print::print_hardware::set_hardware(peripherals.UART);
    let mut timer = Timer::new(peripherals.TIMER0);

    let ll = AmaranthSpw::new(peripherals.SPW_NODE);
    let dll = DataLink::new(&ll);

    dll.set_link_start(true).unwrap();

    loop {
        let state = dll.get_link_state().unwrap();
        println!("State: {:?}", state);

        let credit = dll.get_link_credit().unwrap();
        println!("Credit: {:?}", credit);

        let errors = dll.get_link_error_flags().unwrap();

        if errors.any() {
            println!("Link error: {:?}", errors);
            ll.link_error_clear();
        }

        msleep(&mut timer, 1000);
    }
}

fn msleep(timer: &mut Timer, ms: u32) {
    timer.disable();

    timer.reload(0);
    timer.load(SYSTEM_CLOCK_FREQUENCY / 1_000 * ms);

    timer.enable();

    // Wait until the time has elapsed
    while timer.value() > 0 {}
}
