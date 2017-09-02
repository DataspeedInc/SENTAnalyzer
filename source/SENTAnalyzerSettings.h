#ifndef SENT_ANALYZER_SETTINGS
#define SENT_ANALYZER_SETTINGS

#include <AnalyzerSettings.h>
#include <AnalyzerTypes.h>

class SENTAnalyzerSettings : public AnalyzerSettings
{
public:
	SENTAnalyzerSettings();
	virtual ~SENTAnalyzerSettings();

	virtual bool SetSettingsFromInterfaces();
	void UpdateInterfacesFromSettings();
	virtual void LoadSettings( const char* settings );
	virtual const char* SaveSettings();


	Channel mInputChannel;
	U32 tick_time_half_us;
	bool pausePulseEnabled;
	U32 numberOfDataNibbles;

protected:
	std::auto_ptr< AnalyzerSettingInterfaceChannel >	mInputChannelInterface;
	std::auto_ptr< AnalyzerSettingInterfaceInteger >	tickTimeInterface;
	std::auto_ptr< AnalyzerSettingInterfaceBool >		pausePulseInterface;
	std::auto_ptr< AnalyzerSettingInterfaceInteger >	dataNibblesInterface;
};

#endif //SENT_ANALYZER_SETTINGS
