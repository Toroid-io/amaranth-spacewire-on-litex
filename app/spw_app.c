#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <liblitedram/sdram.h>
#include <libbase/uart.h>
#include <libbase/console.h>

#include <generated/csr.h>
#include <generated/soc.h>

enum link_state {
	ERRORRESET,
	ERRORWAIT,
	READY,
	STARTED,
	CONNECTING,
	RUN
};

static const char *link_state_mapping[] = {
	"ErrorReset", "ErrorWait", "Ready", "Started", "Connecting", "Run"
};

int main(int argc, char* argv[])
{
	enum link_state link_state = ERRORRESET;
	unsigned int link_error = 0;

#ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
#endif
	uart_init();

	printf("Initializing SpaceWire core...\n");
	spw_node_control_link_error_clear_write(1);
	spw_node_control_link_autorecover_write(1);
	spw_node_control_link_start_write(1);

	printf("Waiting link to be ready...\n");

	while(1) {
		printf("Status:\n");
		link_error = spw_node_status_link_error_read();
		printf("\tLink error:\t\t%s\n", link_error ? "yes" : "no");
		link_state = spw_node_status_link_state_read();
		printf("\tLink state:\t\t%s\n", link_state_mapping[link_state]);

		busy_wait(1000);
	}

	return 0;
}
