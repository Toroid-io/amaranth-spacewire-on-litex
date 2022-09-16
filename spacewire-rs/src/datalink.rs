use crate::common::*;

#[derive(Debug)]
pub struct LinkCredit {
    pub tx: u8,
    pub rx: u8
}

#[derive(Debug, PartialEq)]
pub enum LinkState {
    ErrorReset,
    ErrorWait,
    Ready,
    Started,
    Connecting,
    Run
}

#[derive(Debug)]
pub struct LinkError {
    pub disconnect: bool,
    pub parity: bool,
    pub escape: bool,
    pub credit: bool,
    pub disabled: bool,
}

impl LinkError {
    pub fn any(&self) -> bool {
        self.disconnect || self.parity || self.escape || self.credit
    }
    
    pub fn none(&self) -> bool {
        !self.any()
    }
}

#[derive(Debug)]
pub enum DataLinkLayerError {
    UnknownLinkState,
    Error
}

pub struct DataLink<'a, T: LowLevelAccess> {
    ll: &'a T
}

impl<'a, T> DataLink<'a, T>
where T: LowLevelAccess {
    pub fn new(ll: &'a T) -> Self {
        DataLink {
            ll
        }
    }
    
    pub fn set_link_disabled(&self, state: bool) -> Result<(), DataLinkLayerError> {
        self.ll.set_link_disabled(state)
    }
    
    pub fn get_link_disabled(&self) -> Result<bool, DataLinkLayerError> {
        self.ll.get_link_disabled()
    }
    
    pub fn set_link_start(&self, start: bool) -> Result<(), DataLinkLayerError> {
        self.ll.set_link_start(start)
    }

    pub fn get_link_start(&self) -> Result<bool, DataLinkLayerError> {
        self.ll.get_link_start()
    }
    
    pub fn set_link_autostart(&self, start: bool) -> Result<(), DataLinkLayerError> {
        self.ll.set_link_autostart(start)
    }

    pub fn get_link_autostart(&self) -> Result<bool, DataLinkLayerError> {
        self.ll.get_link_autostart()
    }
    
    pub fn get_link_state(&self) -> Result<LinkState, DataLinkLayerError> {
        self.ll.get_link_state()
    }
    
    pub fn get_link_error_flags(&self) -> Result<LinkError, DataLinkLayerError> {
        self.ll.get_link_error_flags()
    }

    pub fn get_link_credit(&self) -> Result<LinkCredit, DataLinkLayerError> {
        self.ll.get_link_credit()
    }
}