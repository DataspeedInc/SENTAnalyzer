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
	double tick_time_us;
	bool pausePulseEnabled;
	U32 numberOfDataNibbles;
	bool spc;
	bool legacyCRC;

protected:
	std::unique_ptr< AnalyzerSettingInterfaceChannel >	mInputChannelInterface;
	std::unique_ptr< AnalyzerSettingInterfaceText >   	tickTimeInterface;
	std::unique_ptr< AnalyzerSettingInterfaceBool >		pausePulseInterface;
	std::unique_ptr< AnalyzerSettingInterfaceInteger >	dataNibblesInterface;
	std::unique_ptr< AnalyzerSettingInterfaceBool >		spcInterface;
	std::unique_ptr< AnalyzerSettingInterfaceBool >		legacyCRCInterface;
};

#endif //SENT_ANALYZER_SETTINGS