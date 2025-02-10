package com.github.pruszko.achievementnotification.achievements
{
	import com.github.pruszko.achievementnotification.AchievementNotificationFlash;
	import com.github.pruszko.achievementnotification.utils.Disposable;
	
	public class AchievementRegistry implements Disposable
	{
		private var _app:AchievementNotificationFlash;
		
		private var _registry:Object;
		
		public function AchievementRegistry(app:AchievementNotificationFlash, serializedAchievementRegistry:Object)
		{
			super();
			this._app = app;
			
			this._registry = new Object();
			
			for (var achievementKey:String in serializedAchievementRegistry)
			{
				var serializedAchievement:Object = serializedAchievementRegistry[achievementKey];
				this._registry[achievementKey] = new Achievement(serializedAchievement);
			}
		}
		
		public function getAchievementByKey(achievementKey:String) : Achievement
		{
			return this._registry[achievementKey];
		}
		
		public function disposeState() : void
		{
			var achievementKey:String;
			
			var achievementKeys:Vector.<String> = new Vector.<String>();
			for (achievementKey in this._registry)
			{
				achievementKeys.push(achievementKey);
			}
			
			for (var i:int = 0; i < achievementKeys.length; ++i)
			{
				achievementKey = achievementKeys[i];
				
				var achievement:Achievement = this._registry[achievementKey];
				achievement.disposeState();
				
				delete this._registry[achievementKey];
			}
			
			this._registry = null;
			achievementKeys.splice(0, achievementKeys.length);
		}
		
	}

}