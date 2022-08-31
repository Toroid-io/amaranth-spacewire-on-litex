include $(BUILD_DIR)/software/include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

#Set target (binary names)
TARGET = spw_app

#Set compiler/linker flags
CXXFLAGS += -I.
OBJECTS = spw_app.o crt0.o

###############################################################

all : $(TARGET).bin

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(TARGET).elf: $(OBJECTS)
	@cp -r $(BUILD_DIR)/software/include/generated .
	$(CC) $(LDFLAGS) \
		-T linker.ld \
		-N -o $@ \
		$(OBJECTS) \
		$(PACKAGES:%=-L$(BUILD_DIR)/software/%) \
		-Wl,--whole-archive \
		-Wl,--gc-sections \
		-Wl,-Map,$@.map \
		$(LIBS:lib%=-l%)

-include $(OBJECTS:.o=.d)

VPATH = $(CPU_DIRECTORY)

crt0.o: $(CPU_DIRECTORY)/crt0.S
	$(assemble)

%.o: %.S
	$(assemble)

%.o: %.c
	$(compile)

%.o: %.cpp
	$(compilexx)

clean :
	rm -rf $(TARGET).bin $(TARGET).elf $(OBJECTS)

.PHONY : all clean
