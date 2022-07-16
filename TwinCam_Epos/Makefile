CC = g++
CFLAGS = -I.
TARGET = TwinCamEpos
LIBS = -lEposCmd -lboost_python3

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) -I/usr/include/python3.6m -DPIC -shared -fPIC -o $(TARGET).so $(TARGET).cpp $(CFLAGS) $(LIBS)

clean:
	$(RM) $(TARGET)
