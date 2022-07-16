//============================================================================
// Name        : TwinCam_EposCmd.cpp
// Author      : Vibol Yem
// Version     : 2022-1-19
//============================================================================

#include <iostream>
#include "Definitions.h"
#include <string.h>
#include <sstream>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>//atof()
#include <stdio.h>
#include <list>
#include <math.h>
#include <cmath>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h> //printf(), perror()
#include <sys/times.h>
#include <sys/time.h>
#include <boost/python.hpp>

typedef void* HANDLE;
typedef int BOOL;


enum EAppMode
{
	AM_UNKNOWN,
	AM_DEMO,
	AM_INTERFACE_LIST,
	AM_PROTOCOL_LIST,
	AM_VERSION_INFO
};


using namespace std;

HANDLE g_pKeyHandle = 0;
unsigned short g_usNodeId = 1;
string g_deviceName;
string g_protocolStackName;
string g_interfaceName;
string g_portName;
int g_baudrate = 0;
EAppMode g_eAppMode = AM_DEMO;

const string g_programName = "TwinCam_EposCmd";

void* TwinCamKeyHandle;
const int TwinCamNodeID = 4;///////////////////////// Node ID for TwinCam = 4 ////////////////////

#ifndef MMC_SUCCESS
	#define MMC_SUCCESS 0
#endif

#ifndef MMC_FAILED
	#define MMC_FAILED 1
#endif

#ifndef MMC_MAX_LOG_MSG_SIZE
	#define MMC_MAX_LOG_MSG_SIZE 512
#endif

void  LogError(string functionName, int p_lResult, unsigned int p_ulErrorCode);
void  LogInfo(string message);
void  SeparatorLine();
void  SetDefaultParameters();
int  OpenDevice(unsigned int* p_pErrorCode);
int  CloseDevice(unsigned int* p_pErrorCode);

int  PrintAvailableInterfaces();
int  PrintAvailablePortsAndOpenDevice(char* p_pInterfaceNameSel);
int  Reset();
int  Disable();
int  PrintAvailableProtocols();
int  PrintDeviceVersionWithNodeID();

int activateTwinCamPostionMode();
int setTwinCamPostionAndVelocity(double deg, double degPerSec, double degPerSecSec);
int initTwinCam();
int closeAllDevices();


void LogError(string functionName, int p_lResult, unsigned int p_ulErrorCode)
{
	cerr << g_programName << ": " << functionName << " failed (result=" << p_lResult << ", errorCode=0x" << std::hex << p_ulErrorCode << ")"<< endl;
}

void LogInfo(string message)
{
	cout << message << endl;
}

void SeparatorLine()
{
	const int lineLength = 65;
	for(int i=0; i<lineLength; i++)
	{
		cout << "-";
	}
	cout << endl;
}

void SetDefaultParameters()
{
	//USB
	g_usNodeId = 1;
	g_deviceName = "EPOS4";
	g_protocolStackName = "MAXON SERIAL V2";
	g_interfaceName = "USB";
	g_portName = "USB0";
	g_baudrate = 1000000;
}

int OpenDevice()
{
    int lResult = MMC_SUCCESS;//MMC_FAILED;
	unsigned int ulErrorCode = 0;
	char* pDeviceName = new char[255];
	char* pProtocolStackName = new char[255];
	char* pInterfaceName = new char[255];
	char* pPortName = new char[255];

	strcpy(pDeviceName, g_deviceName.c_str());
	strcpy(pProtocolStackName, g_protocolStackName.c_str());
	strcpy(pInterfaceName, g_interfaceName.c_str());
	strcpy(pPortName, g_portName.c_str());

	LogInfo("Open device...");
	LogInfo(g_deviceName);
	LogInfo(g_protocolStackName);
	LogInfo(g_interfaceName);
	LogInfo(g_portName);

	g_pKeyHandle = VCS_OpenDevice(pDeviceName, pProtocolStackName, pInterfaceName, pPortName, &ulErrorCode);

	if(g_pKeyHandle!=0 && ulErrorCode == 0)
	{
		lResult = MMC_SUCCESS;
		LogInfo("Open device success");
	}
	else
	{
		g_pKeyHandle = 0;
	}

	delete []pDeviceName;
	delete []pProtocolStackName;
	delete []pInterfaceName;
	delete []pPortName;

	return lResult;
}

int CloseDevice(unsigned int* p_pErrorCode)
{
	int lResult = MMC_FAILED;

	*p_pErrorCode = 0;

	LogInfo("Close device");

	if(VCS_CloseDevice(g_pKeyHandle, p_pErrorCode)!=0 && *p_pErrorCode == 0)
	{
		lResult = MMC_SUCCESS;
	}

	return lResult;
}


//port name (COM1, USB0, CAN0,... default - USB0)"
//Open device check version
int PrintAvailablePortsAndOpenDevice(char* p_pInterfaceNameSel) //this function is called in initTwinCam()
{
	int lResult = MMC_FAILED;
	int lStartOfSelection = 1;
	int lMaxStrSize = 255;
	char* pPortNameSel = new char[lMaxStrSize];
	int lEndOfSelection = 0;
	unsigned int ulErrorCode = 0;

	do
	{
		//g_deviceName = "EPOS4"; g_protocolStackName = "MAXON SERIAL V2"; g_interfaceName = "USB";
		if(!VCS_GetPortNameSelection((char*)g_deviceName.c_str(), (char*)g_protocolStackName.c_str(), p_pInterfaceNameSel, lStartOfSelection, pPortNameSel, lMaxStrSize, &lEndOfSelection, &ulErrorCode))
		{
			lResult = MMC_FAILED;
			LogError("GetPortNameSelection", lResult, ulErrorCode);
			break;
		}
		else //if there is a port name found (USB0 or USB1...)
		{
			printf("usb port = %s\n", pPortNameSel);
			//opend device and check device version if node id is correct
			g_portName = std::string(pPortNameSel); //get port name (USB0 or USB1...)
			if(PrintDeviceVersionWithNodeID() == MMC_SUCCESS) //Open device and print device version
				lResult = MMC_SUCCESS;
		}

		lStartOfSelection = 0;
	}
	while(lEndOfSelection == 0);

	return lResult;
}

//Open device and print device version
int PrintDeviceVersionWithNodeID()
{
	int lResult = MMC_FAILED;
	unsigned short usHardwareVersion = 0;
	unsigned short usSoftwareVersion = 0;
	unsigned short usApplicationNumber = 0;
	unsigned short usApplicationVersion = 0;
	unsigned int ulErrorCode = 0;

	//Open device before checking version, port name is required but not nodeID
	if((lResult = OpenDevice())!=MMC_SUCCESS)//if it is failed to Open Device
	{
		LogError("OpenDevice failed", lResult, ulErrorCode);
		//return lResult;
	}

	//checking version refer to node id
	//TwinCamNodeID = 4

	if(VCS_GetVersion(g_pKeyHandle, TwinCamNodeID, &usHardwareVersion, &usSoftwareVersion, &usApplicationNumber, &usApplicationVersion, &ulErrorCode))
	{
        	TwinCamKeyHandle = g_pKeyHandle;
		printf("%s Hardware Version    = 0x%04x\n      Software Version    = 0x%04x\n      Application Number  = 0x%04x\n      Application Version = 0x%04x\n",
			g_deviceName.c_str(), usHardwareVersion, usSoftwareVersion, usApplicationNumber, usApplicationVersion);
		lResult = MMC_SUCCESS;
	}
	else{
		LogInfo("Can not get device version");
		CloseDevice(&ulErrorCode);
		SeparatorLine();

	}

	return lResult;
}



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//interface name (RS232, USB, CAN_ixx_usb 0, CAN_kvaser_usb 0,... default - USB)"
//port name (COM1, USB0, CAN0,... default - USB0)"
//Open Device check version
int PrintAvailableInterfaces()
{
	int lResult = MMC_FAILED;
	int lStartOfSelection = 1;
	int lMaxStrSize = 255;
	char* pInterfaceNameSel = new char[lMaxStrSize];
	int lEndOfSelection = 0;
	unsigned int ulErrorCode = 0;

	do
	{
		if(!VCS_GetInterfaceNameSelection((char*)g_deviceName.c_str(), (char*)g_protocolStackName.c_str(), lStartOfSelection, pInterfaceNameSel, lMaxStrSize, &lEndOfSelection, &ulErrorCode))
		{
			lResult = MMC_FAILED;
			LogError("GetInterfaceNameSelection", lResult, ulErrorCode);
			break;
		}
		else
		{
			lResult = MMC_SUCCESS;

			printf("interface = %s\n", pInterfaceNameSel);

			PrintAvailablePortsAndOpenDevice(pInterfaceNameSel);//Open device and print device version
		}

		lStartOfSelection = 0;
	}
	while(lEndOfSelection == 0);

	SeparatorLine();

	delete[] pInterfaceNameSel;

	return lResult;
}

//protocol stack name (MAXON_RS232, CANopen, MAXON SERIAL V2, default - MAXON SERIAL V2)
//interface name (RS232, USB, CAN_ixx_usb 0, CAN_kvaser_usb 0,... default - USB)"
//port name (COM1, USB0, CAN0,... default - USB0)"
int PrintAvailableProtocols()
{
	int lResult = MMC_FAILED;
	int lStartOfSelection = 1;
	int lMaxStrSize = 255;
	char* pProtocolNameSel = new char[lMaxStrSize];
	int lEndOfSelection = 0;
	unsigned int ulErrorCode = 0;

	do
	{
		if(!VCS_GetProtocolStackNameSelection((char*)g_deviceName.c_str(), lStartOfSelection, pProtocolNameSel, lMaxStrSize, &lEndOfSelection, &ulErrorCode))
		{
			lResult = MMC_FAILED;
			LogError("GetProtocolStackNameSelection", lResult, ulErrorCode);
			break;
		}
		else
		{
			lResult = MMC_SUCCESS;

			printf("protocol stack name = %s\n", pProtocolNameSel);
			PrintAvailableInterfaces();//interface name and port name
		}

		lStartOfSelection = 0;
	}
	while(lEndOfSelection == 0);

	SeparatorLine();

	delete[] pProtocolNameSel;

	return lResult;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////




int Reset()
{
	unsigned int ulErrorCode = 0;
	int lResult = MMC_FAILED;
	if(!VCS_SetDisableState(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
	{
        if(!VCS_ClearFault(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
		{
            if(!VCS_SetEnableState(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
			{
				//LogInfo(TwinCamNodeID);
				LogInfo("Reset TwinCam Epos Success");
                return MMC_SUCCESS;
			}
		}
	}
	LogInfo("Reset TwinCam Epos Failed");
	return lResult;
}

int Disable()
{
    unsigned int ulErrorCode = 0;
    int lResult = MMC_FAILED;
    if(!VCS_SetDisableState(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
    {
    	LogInfo("Disable TwinCam Epos Success");
		return MMC_SUCCESS;
    }
    LogInfo("Disable TwinCam Epos Failed");
    return MMC_FAILED;
}

int Enable()
{
    unsigned int ulErrorCode = 0;
    int lResult = MMC_FAILED;
    if(!VCS_SetEnableState(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
    {
    	LogInfo("Enable TwinCam Epos Success");
		return MMC_SUCCESS;
    }
    LogInfo("Enable TwinCam Epos Failed");
    return MMC_FAILED;
}

int activateTwinCamPostionMode()
{
        unsigned int ulErrorCode = 0;
        if(!VCS_ActivateProfilePositionMode(TwinCamKeyHandle, TwinCamNodeID, &ulErrorCode))
	{
			LogInfo("activateTwinCamPostionMode");
	        return MMC_SUCCESS;
	}
	return MMC_FAILED;
}


const int gearRatio = 1;
const int pulsePerRound = 2000;
int setTwinCamPostionAndVelocity(double deg, double degPerSec, double degPerSecSec){
	unsigned int ulErrorCode = 0;

	int pos = (int)(pulsePerRound * 180 * deg / M_PI); //deg to num of pulse
	int vel = (int)(degPerSec / 6.0); //deg per second to round per minune (rpm) 60.0 * degPerSec / 360.0
	int acel = (int)(degPerSecSec / 6.0); //degPerSecSec to rpm/s
	if(!VCS_SetPositionProfile(TwinCamKeyHandle, TwinCamNodeID, vel, acel, acel, &ulErrorCode))
		if(!VCS_MoveToPosition(TwinCamKeyHandle, TwinCamNodeID, pos, 1, 1, &ulErrorCode))
			return 1;

	return 0;
}


//int main(int argc, char** argv)
int initTwinCam()
{
	unsigned int ulErrorCode = 0;
	SetDefaultParameters();
	//VCS_CloseAllDevices(&ulErrorCode);

	SeparatorLine();
	PrintAvailableInterfaces();
	SeparatorLine();
/*
	if(PrintAvailablePortsAndOpenDevice((char*)g_interfaceName.c_str()) == MMC_FAILED){//USB
		printf("No EPOS\n");
		return 0;
	}
        if(Reset() == MMC_FAILED){
		printf("Unable Reset EPOS\n");
		return 0;
	}
*/
    if(activateTwinCamPostionMode() == MMC_FAILED){
		printf("Unable set EPOS mode\n");
		return 0;
	}

	sleep(1);
	return 1;
}

int closeAllDevices()
{
	unsigned int ulErrorCode = 0;
	VCS_CloseAllDevices(&ulErrorCode);

	return 1;
}

BOOST_PYTHON_MODULE(TwinCamEpos) {
	using namespace boost::python;
	def("initTwinCam", &initTwinCam);
	def("closeAllDevices",&closeAllDevices);
	def("setTwinCamPostionAndVelocity", &setTwinCamPostionAndVelocity);
    def("Disable", &Disable);
	def("Enable", &Enable);
    def("Reset", &Reset);

}
