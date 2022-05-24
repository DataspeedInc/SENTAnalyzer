#ifndef SENT_SIMULATION_DATA_GENERATOR
#define SENT_SIMULATION_DATA_GENERATOR

#include <SimulationChannelDescriptor.h>
#include <string>
class SENTAnalyzerSettings;

class SENTSimulationDataGenerator
{
public:
	SENTSimulationDataGenerator();
	~SENTSimulationDataGenerator();

	void Initialize( U32 simulation_sample_rate, SENTAnalyzerSettings* settings );
	U32 GenerateSimulationData( U64 newest_sample_requested, U32 sample_rate, SimulationChannelDescriptor** simulation_channel );

protected:
	SENTAnalyzerSettings* mSettings;
	U32 mSimulationSampleRateHz;

protected:
	void CreateSerialByte();
	void AddNibble(U16 number_of_ticks, U16 samples_per_tick);
	void AddSPCTrigger(U16 number_of_low_ticks, U16 samples_per_tick);

	SimulationChannelDescriptor mSerialSimulationData;

	U8 mSPCDevice;

};
#endif //SENT_SIMULATION_DATA_GENERATOR