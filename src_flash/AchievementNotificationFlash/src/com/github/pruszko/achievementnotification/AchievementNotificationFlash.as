package com.github.pruszko.achievementnotification
{
	import com.github.pruszko.achievementnotification.achievements.Achievement;
	import com.github.pruszko.achievementnotification.achievements.AchievementNotification;
	import com.github.pruszko.achievementnotification.achievements.AchievementRegistry;
	import com.github.pruszko.achievementnotification.config.Config;
	import com.github.pruszko.achievementnotification.queue.NotificationBar;
	import flash.display.Sprite;
	import flash.events.Event;
	
	public class AchievementNotificationFlash extends Sprite
	{

		private static const SWF_HALF_WIDTH:Number = 400;
		private static const SWF_HALF_HEIGHT:Number = 300;
		
		private var _screenWidth:int = 0;
		private var _screenHeight:int = 0;
		private var _scale:Number = 1.0;
		
		private var _achievementRegistry:AchievementRegistry = null;
		private var _notificationBar:NotificationBar;
		
		private var _config:Config = new Config();
		
		public function AchievementNotificationFlash()
		{
			super();
			
			this._notificationBar = new NotificationBar(this);
			this.addChild(this._notificationBar);
		}
		
		public function as_populate() : void
		{
			
		}
		
		public function as_dispose() : void
		{
			this._achievementRegistry.disposeState();
		}
		
		public function as_applyAchievementRegistry(serializedAchievementRegistry:Object) : void
		{
			this._achievementRegistry = new AchievementRegistry(this, serializedAchievementRegistry)
		}
		
		public function as_applyConfig(serializedConfig:Object) : void
		{
			this._config.deserialize(serializedConfig);
		}
		
		public function as_onRecreateDevice(screenWidth:int, screenHeight:int, scale:Number) : void
		{
			this._screenWidth = screenWidth;
			this._screenHeight = screenHeight;
			this._scale = scale;
			
			// This is based on updatePosition() from battleDamageIndicatorApp.swf
			// because it is the only source of "something is working" stuff 
			// and "visible in code" stuff when it comes to GUI.Flash
			//
			// Basically, our flash app center is positioned in the middle of the screen
			// with width and height declared in swf file
			// and despite having settings to change this behavior (position, size, anchors, etc)
			// from python-side on GUI.Flash, those does not work at all, lmao
			// 
			// To fix it ourselves, we have to:
			// - add half size of swf to anchor it to its left top corner in the middle of the screen
			// - substract half of the screen to move it to left top corner of the screen
			// 
			// Those changes MUST be done on flash object itself, not on GUI.Flash component
			this.x = SWF_HALF_WIDTH - (screenWidth / 2.0);
			this.y = SWF_HALF_HEIGHT - (screenHeight / 2.0);
			
			this._notificationBar.x = (screenWidth / 2.0) - (this._notificationBar.estimatedWidgetWidth * this._scale / 2.0);
			this._notificationBar.y = this.config.verticalPosition * screenHeight;
			this._notificationBar.scaleX = this._scale;
			this._notificationBar.scaleY = this._scale;
		}
		
		public function as_displayAchievement(achievementKey:String, extended:Boolean) : void
		{
			var achievement:Achievement = this._achievementRegistry.getAchievementByKey(achievementKey);
			var achievementNotification:AchievementNotification = new AchievementNotification(this, achievement, extended);
			
			this._notificationBar.addNotification(achievementNotification);
		}
		
		public function get config() : Config
		{
			return this._config;
		}
		
		public function get scale() : Number
		{
			return this._scale;
		}
		
	}
	
}