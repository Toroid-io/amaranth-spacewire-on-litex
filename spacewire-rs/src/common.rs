use crate::datalink::*;

pub trait LowLevelAccess {
    fn port_reset(&self) -> Result<(), DataLinkLayerError>;
    fn set_link_disabled(&self, disabled: bool) -> Result<(), DataLinkLayerError>;
    fn get_link_disabled(&self) -> Result<bool, DataLinkLayerError>;
    fn get_link_start(&self) -> Result<bool, DataLinkLayerError>;
    fn set_link_start(&self, start: bool) -> Result<(), DataLinkLayerError>;
    fn get_link_autostart(&self) -> Result<bool, DataLinkLayerError>;
    fn set_link_autostart(&self, start: bool) -> Result<(), DataLinkLayerError>;
    fn get_link_state(&self) -> Result<LinkState, DataLinkLayerError>;
    fn get_link_error_flags(&self) -> Result<LinkError, DataLinkLayerError>;
    fn get_link_credit(&self) -> Result<LinkCredit, DataLinkLayerError>;
}