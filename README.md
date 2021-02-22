# KuaveyAdsKit
Huawei Ads Kit adaptation for Python / Kivy. Structurally inspired from [KivMob by Michael Stott](https://github.com/MichaelStott/KivMob)

## Warning!
*Currently only Rewarded Ads format supported! Other formats will be added over time.*

## Installation

1) Just add `KuaveyAdsKit.py` to your Kivy project root.

2) Download the appropriate ADS SDK from the Huawei Developers website. Like `adssdk-eclipse-3.4.37.300.zip` from [that developer.huawei.com page](https://developer.huawei.com/consumer/en/doc/development/HMSCore-Library-V5/eclipse-sdk-download-0000001050064958-V5).

3) Extract the JAR files from the archive (only JAR files are needed).
The following JAR files should appear in your project:
* **ads-base.jar** (root JAR file for the entire SDK)
* **ads-reward.jar**

*Other JAR files are not used by the KuaveyAdsKit yet!*

For convenience, put these JAR files in a separate folder in your project, for example, in the `adskit` folder.

4) Add to your `buildozer.spec` file links to these JARs, like:

```python
android.add_jars = adskit/*.jar
```

## Using

### Rewarded Ads

1) Import `KuaveyAdsKit` and `HmsRewardAdListenerInterface` classes:
```python
...
if platform == 'android':
    from KuaveyAdsKit import KuaveyAdsKit, HmsRewardAdListenerInterface
....
````

2) Inherit the `HmsRewardAdListenerInterface` into a new class to override the methods (if you want to track the ad showing status and perform some action):
```python
...
    class HmsRewardsHandler(HmsRewardAdListenerInterface):
        def on_rewarded(self, paramReward):
            # do_something()
            print("Thanks for watching donation.")
        
        def on_reward_ad_closed(self):
            # do_something()
            print("You didn't wait for the ad to end")
        
        def on_reward_ad_failed_to_load(self, paramInt):
            print("Error code:", paramInt)
        
        def on_reward_ad_left_app(self):
            pass
        
        def on_reward_ad_loaded(self):
            pass
        
        def on_reward_ad_opened(self):
            pass
        
        def on_reward_ad_completed(self):
            pass
        
        def on_reward_ad_started(self):
            pass
...
```

3) Initialize the `KuaveyAdsKit` and load ads, specifying the ID and new listening interface as arguments.
```python
...
    hms_ads = KuaveyAdsKit()
    hms_ads.load_rewarded_ad("testx9dtjwj8hp", HmsRewardsHandler())
...
```

4) Show ads where needed:
```python
...
    hms_ads.show_reward_ad()
...
```

5) Don't forget to load ads after returning to kivy activity:
```python
...
class MyKivyApp(App):
...
    def on_resume(self):
        hms_ads.load_rewarded_ad("testx9dtjwj8hp", HmsRewardsHandler())
...
```
