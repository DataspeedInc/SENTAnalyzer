#include "SENTAnalyzerSettings.h"
#include <AnalyzerHelpers.h>
#include <iomanip>
#include <sstream>
#include <cmath>

SENTAnalyzerSettings::SENTAnalyzerSettings()
:	mInputChannel( UNDEFINED_CHANNEL ),
	tick_time_us(3),
	pausePulseEnabled(true),
	spc(false),
     ignoreCRC(false),
	legacyCRC(false),
	numberOfDataNibbles(6),
	SCGeneration(SCGenerationOptions::Short)
{
	mInputChannelInterface.reset( new AnalyzerSettingInterfaceChannel() );
	mInputChannelInterface->SetTitleAndTooltip( "Serial", "Standard SENT (SAE J2716)" );
	mInputChannelInterface->SetChannel( mInputChannel );

	tickTimeInterface.reset( new AnalyzerSettingInterfaceText() );
	tickTimeInterface->SetTitleAndTooltip( "Tick time (us)", "Specify the SENT tick time in microseconds" );
	std::stringstream tick_time_text;
	tick_time_text << std::fixed << std::setprecision(2) << tick_time_us;
	tickTimeInterface->SetText( tick_time_text.str().c_str() );

	dataNibblesInterface.reset( new AnalyzerSettingInterfaceInteger() );
	dataNibblesInterface->SetTitleAndTooltip( "Number of data nibbles", "Specify the total number of fast channel data nibbles" );
	dataNibblesInterface->SetMax( 6 );
	dataNibblesInterface->SetMin( 0 );
	dataNibblesInterface->SetInteger( numberOfDataNibbles );

	spcInterface.reset( new AnalyzerSettingInterfaceBool() );
	spcInterface->SetTitleAndTooltip( "SPC", "Specify whether the signal is using the SPC extension or not" );
	spcInterface->SetValue(spc);

	pausePulseInterface.reset( new AnalyzerSettingInterfaceBool() );
	pausePulseInterface->SetTitleAndTooltip( "Pause pulse", "Specify whether pause pulse is enabled or not" );
	pausePulseInterface->SetValue(pausePulseEnabled);

	ignoreCRCInterface.reset( new AnalyzerSettingInterfaceBool() );
	ignoreCRCInterface->SetTitleAndTooltip( "Ignore CRC", "Specify whether the crc should be done or not" );
	ignoreCRCInterface->SetValue(ignoreCRC);

	legacyCRCInterface.reset( new AnalyzerSettingInterfaceBool() );
	legacyCRCInterface->SetTitleAndTooltip( "Legacy CRC", "Specify whether the legacy crc calculation should be used or not" );
	legacyCRCInterface->SetValue(legacyCRC);

	AddInterface( mInputChannelInterface.get() );
	AddInterface( tickTimeInterface.get() );
	AddInterface( dataNibblesInterface.get() );
	AddInterface( spcInterface.get() );
	AddInterface( pausePulseInterface.get() );
     AddInterface( ignoreCRCInterface.get() );
	AddInterface( legacyCRCInterface.get() );

	// Generation tools //
	#ifdef GENERATION_TOOLS
	SCGenerationInterface.reset( new AnalyzerSettingInterfaceNumberList() );
	SCGenerationInterface->SetTitleAndTooltip( "Slow channel generation format", 
		"Specify which format will be generated into the slow-channel while generating in demo mode." );
	SCGenerationInterface->AddNumber( SCGenerationOptions::Short, "Short Format", "Short Serial Message Format" );
	SCGenerationInterface->AddNumber( SCGenerationOptions::Enhanced, "Enhanced Format", "Enhanced Serial Message Format" );

	AddInterface( SCGenerationInterface.get() );
	#endif

	AddExportOption( 0, "Export as text/csv file" );
	AddExportExtension( 0, "text", "txt" );
	AddExportExtension( 0, "csv", "csv" );

	ClearChannels();
	AddChannel( mInputChannel, "Serial", false );
}

SENTAnalyzerSettings::~SENTAnalyzerSettings()
{
}

bool SENTAnalyzerSettings::SetSettingsFromInterfaces()
{
	mInputChannel = mInputChannelInterface->GetChannel();

	try {
		tick_time_us = atof(tickTimeInterface->GetText());
		// Round tick_time_us to two decimal places of precision.
		tick_time_us = round(tick_time_us * 100) / 100;
	} catch (...) {
		std::stringstream e;
		e << "Tick time invalid: " << tickTimeInterface->GetText();
		throw std::runtime_error(e.str().c_str());
	}

	spc = spcInterface->GetValue();
	// The pause pulse is always used if using SPC, as part of SPC spec.
	pausePulseEnabled = spc ? true : pausePulseInterface->GetValue();

	numberOfDataNibbles = dataNibblesInterface->GetInteger();
	legacyCRC = legacyCRCInterface->GetValue();
     ignoreCRC = ignoreCRCInterface->GetValue();

	#ifdef GENERATION_TOOLS
	SCGeneration = (SCGenerationOptions)SCGenerationInterface->GetNumber();
	#endif

	ClearChannels();
	AddChannel( mInputChannel, "SENT (SAE J2716)", true );

	return true;
}

void SENTAnalyzerSettings::UpdateInterfacesFromSettings()
{
	mInputChannelInterface->SetChannel(mInputChannel);
	
	std::stringstream tick_time_text;
	tick_time_text << std::fixed << std::setprecision(2) << tick_time_us;
	tickTimeInterface->SetText(tick_time_text.str().c_str());

	dataNibblesInterface->SetInteger(numberOfDataNibbles);
	legacyCRCInterface->SetValue(spc);
	pausePulseInterface->SetValue(pausePulseEnabled);
	legacyCRCInterface->SetValue(legacyCRC);
     ignoreCRCInterface->SetValue(ignoreCRC);
}

void SENTAnalyzerSettings::LoadSettings( const char* settings )
{
	SimpleArchive text_archive;
	text_archive.SetString( settings );

	text_archive >> mInputChannel;
	text_archive >> tick_time_us;
	text_archive >> numberOfDataNibbles;
	text_archive >> spc;
	text_archive >> pausePulseEnabled;
	text_archive >> legacyCRC;

	ClearChannels();
	AddChannel( mInputChannel, "SENT (SAE J2716)", true );

	UpdateInterfacesFromSettings();
}

const char* SENTAnalyzerSettings::SaveSettings()
{
	SimpleArchive text_archive;

	text_archive << mInputChannel;
	text_archive << tick_time_us;
	text_archive << numberOfDataNibbles;
	text_archive << spc;
	text_archive << pausePulseEnabled;
	text_archive << legacyCRC;

	return SetReturnString( text_archive.GetString() );
}
