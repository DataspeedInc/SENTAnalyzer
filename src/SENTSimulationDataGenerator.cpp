#include "SENTSimulationDataGenerator.h"
#include "SENTAnalyzerSettings.h"

#include <AnalyzerHelpers.h>

const int fc_data [6] = {7, 4, 8, 7, 4, 8};
const int device_ticks [4] = {11, 21, 38, 65};

SENTSimulationDataGenerator::SENTSimulationDataGenerator()
{
	mSPCDevice = 0;
}

SENTSimulationDataGenerator::~SENTSimulationDataGenerator()
{
}

void SENTSimulationDataGenerator::Initialize( U32 simulation_sample_rate, SENTAnalyzerSettings* settings )
{
	mSimulationSampleRateHz = simulation_sample_rate;
	mSettings = settings;

	mSerialSimulationData.SetChannel( settings->mInputChannel );
	mSerialSimulationData.SetSampleRate( simulation_sample_rate );
	mSerialSimulationData.SetInitialBitState( BIT_HIGH );
}

U32 SENTSimulationDataGenerator::GenerateSimulationData( U64 largest_sample_requested, U32 sample_rate, SimulationChannelDescriptor** simulation_channel )
{
	U64 adjusted_largest_sample_requested = AnalyzerHelpers::AdjustSimulationTargetSample( largest_sample_requested, sample_rate, mSimulationSampleRateHz );

	while( mSerialSimulationData.GetCurrentSampleNumber() < adjusted_largest_sample_requested )
	{
		CreateSerialByte();
	}

	*simulation_channel = &mSerialSimulationData;
	return 1;
}

void SENTSimulationDataGenerator::AddNibble(U16 number_of_ticks, U16 samples_per_tick)
{
	U16 number_of_high_ticks = number_of_ticks - 5;
	mSerialSimulationData.Transition();
	mSerialSimulationData.Advance( samples_per_tick * 5);
	mSerialSimulationData.Transition();
	mSerialSimulationData.Advance( samples_per_tick * number_of_high_ticks);
}

void SENTSimulationDataGenerator::AddSPCTrigger(U16 number_of_low_ticks, U16 samples_per_tick)
{
	U16 number_of_high_ticks = 100 - number_of_low_ticks;
	mSerialSimulationData.Transition();
	mSerialSimulationData.Advance( samples_per_tick * number_of_low_ticks);
	mSerialSimulationData.Transition();
	mSerialSimulationData.Advance( samples_per_tick * number_of_high_ticks );
}

void SENTSimulationDataGenerator::CreateSerialByte()
{
	U32 samples_per_tick = (mSimulationSampleRateHz * mSettings->tick_time_us) / 1000000;

	if ( mSettings->pausePulseEnabled )
	{
	    /* First, a normal SENT frame */

		/* Master Trigger Pulse - Cycles through device IDs */
		if ( mSettings->spc )
		{
			AddSPCTrigger(device_ticks[mSPCDevice++], samples_per_tick);
			mSPCDevice = mSPCDevice % 4;
		}
		/* Calibration pulse */
		AddNibble(56, samples_per_tick);
		/* Status nibble */
		AddNibble(12, samples_per_tick);
		/* Fast channel nibbles */
		for (U8 counter = 0; counter < mSettings->numberOfDataNibbles; counter++) {
			AddNibble(fc_data[counter] + 12, samples_per_tick);
		}
		/* CRC */
		AddNibble(12 + 3, samples_per_tick);
		/* Pause pulse */
		AddNibble(100, samples_per_tick);

		/* Then, another valid SENT frame, but with a pause pulse the size of a sync pulse. Muhahahahaa */

		/* Master Trigger Pulse - Cycles through device IDs */
		if ( mSettings->spc )
		{
			AddSPCTrigger(device_ticks[mSPCDevice++], samples_per_tick);
			mSPCDevice = mSPCDevice % 4;
		}
		/* Calibration pulse */
		AddNibble(56, samples_per_tick);
		/* Status nibble */
		AddNibble(12, samples_per_tick);
		/* Fast channel nibbles */
		for (U8 counter = 0; counter < mSettings->numberOfDataNibbles; counter++) {
			AddNibble(fc_data[counter] + 12, samples_per_tick);
		}
		/* CRC */
		AddNibble(12 + 3, samples_per_tick);
		/* Pause pulse */
		AddNibble(56, samples_per_tick);
	}
	else
	{
		/* Then, a valid SENT frame without a pause pulse at the end.
		/* Calibration pulse */
		AddNibble(56, samples_per_tick);
		/* Status nibble */
		AddNibble(12, samples_per_tick);
		/* Fast channel nibbles */
		for (U8 counter = 0; counter < mSettings->numberOfDataNibbles; counter++) {
			AddNibble(fc_data[counter] + 12, samples_per_tick);
		}
		/* CRC */
		AddNibble(12 + 3, samples_per_tick);
	}
}


