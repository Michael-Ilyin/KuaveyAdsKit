import kivy
from kivy.utils import platform
from kivy.logger import Logger

if platform == "android":
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        
        activity = autoclass("org.kivy.android.PythonActivity")
        HwAds = autoclass('com.huawei.hms.ads.HwAds')
        AdParam = autoclass('com.huawei.hms.ads.AdParam')
        AdParam_Builder = autoclass('com.huawei.hms.ads.AdParam$Builder')
        RewardAd = autoclass('com.huawei.hms.ads.reward.RewardAd')
        RewardAdLoadListener = autoclass('com.huawei.hms.ads.reward.RewardAdLoadListener')
        
        class HmsRewardAdListener(PythonJavaClass):
            __javainterfaces__ = (
                "com/huawei/hms/ads/reward/RewardAdListener",
            )
            __javacontext__ = "app"

            def __init__(self, interface):
                self._interface = interface
        
            @java_method("(Lcom/huawei/hms/ads/reward/Reward;)V")
            def onRewarded(self, paramReward):
                self._interface.on_rewarded(paramReward)
        
            @java_method("()V")
            def onRewardAdClosed(self):
                self._interface.on_reward_ad_closed()
        
            @java_method("(I)V")
            def onRewardAdFailedToLoad(self, paramInt):
                self._interface.on_reward_ad_failed_to_load(paramInt)
        
            @java_method("()V")
            def onRewardAdLeftApp(self):
                self._interface.on_reward_ad_left_app()
        
            @java_method("()V")
            def onRewardAdLoaded(self):
                self._interface.on_reward_ad_loaded()
        
            @java_method("()V")
            def onRewardAdOpened(self):
                self._interface.on_reward_ad_opened()
        
            @java_method("()V")
            def onRewardAdCompleted(self):
                self._interface.on_reward_ad_completed()

            @java_method("()V")
            def onRewardAdStarted(self):
                self._interface.on_reward_ad_started()
    except BaseException:
        Logger.error(
            "KuaveyAdsKit: Cannot load AdsKit classes. Check buildozer.spec."
        )
else:
    class HmsRewardAdListener:
        pass

    def run_on_ui_thread(x):
        pass

class HmsRewardAdListenerInterface:
    """ Interface for objects that handle rewarded video ad callback functions
    """

    def on_rewarded(self, paramReward):
        pass

    def on_reward_ad_closed(self):
        pass

    def on_reward_ad_failed_to_load(self, paramInt):
        pass

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

class HmsAdsBridge:
    @run_on_ui_thread
    def __init__(self):
        HwAds.init(activity.mActivity)

    @run_on_ui_thread
    def load_rewarded_ad(self, AD_ID, interface):
        self._rewad = RewardAd(activity.mActivity, AD_ID)
        self._rewad.loadAd(AdParam_Builder().build(), RewardAdLoadListener())
        self._listener = HmsRewardAdListener(interface)
        self._rewad.setRewardAdListener(self._listener)

    @run_on_ui_thread
    def show_reward_ad(self):
        if self._rewad.isLoaded():
            self._rewad.show()

class KuaveyAdsKit:
    """ Allows access to Huawei Ads Kit functionality on Android devices.
    """

    def __init__(self):
        self.bridge = HmsAdsBridge()

    def load_rewarded_ad(self, AD_ID, interface):
        """ Loads rewarded ad. For test case use id: "testx9dtjwj8hp"

            :type AD_ID: string
            :param AD_ID: Huawei Ads Kit rewarded video ID for mobile application.
            :type interface: HmsRewardAdListenerInterface
            :param interface: instance of the class that must be inherited from HmsRewardAdListenerInterface to override its methods.
        """
        self.bridge.load_rewarded_ad(AD_ID, interface)

    def show_reward_ad(self):
        self.bridge.show_reward_ad()

if __name__ == "__main__":
    print("Huawei Ads Kit adaptation for Kivy\n")
    print("(based on KivMob by Michael Stott)\n")
    print("Mikhail Ilyin, 2021\n")