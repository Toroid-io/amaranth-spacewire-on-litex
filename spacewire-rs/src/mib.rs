use crate::common::LowLevelAccess;
use crate::datalink::*;

pub struct MIB<'a, T: LowLevelAccess> {
    ll: &'a T
}

impl<'a, T> MIB<'a, T>
where T: LowLevelAccess {
    pub fn new(ll: &'a T) -> Self {
        MIB {
            ll
        }
    }
    
    pub fn get_link_state(&self) -> Result<LinkState, DataLinkLayerError> {
        self.ll.get_link_state()
    }
    
    pub fn get_errors(&self) -> Option<LinkError> {
        None
    }
}