package com.github.pruszko.achievementnotification.achievements
{
	import com.github.pruszko.achievementnotification.AchievementNotificationFlash;
	import com.github.pruszko.achievementnotification.utils.Disposable;
	import flash.display.Loader;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.net.URLRequest;
	import flash.text.AntiAliasType;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFieldType;
	import flash.text.TextFormat;

	public class AchievementNotification extends Sprite implements Disposable
	{
		
		private static const ICON_SIZE:int = 100;
		private static const TEXT_WIDTH:int = 600;
		
		public static const WIDGET_WIDTH:int = ICON_SIZE + TEXT_WIDTH;
		
		private var _app:AchievementNotificationFlash;
		
		public var displayTime:Number;
		
		private var _largeIcon:Loader;
		private var _conditionalStarTextField:TextField;
		private var _achievementNameTextField:TextField;
		private var _achievementDescriptionTextField:TextField;
		private var _achievementConditionTextField:TextField;
		
		public function AchievementNotification(app:AchievementNotificationFlash, achievement:Achievement, extended:Boolean)
		{
			super();
			this._app = app;
			
			// loading an icon takes time - it's fast, but after calling load(...) we don't have fully proper dimensions yet
			// wait for loading and call this.onIconLoadingComplete(...) to finish positioning
			this._largeIcon = new Loader();
			this._largeIcon.contentLoaderInfo.addEventListener(Event.COMPLETE, this.onIconLoadingComplete);
			this._largeIcon.load(new URLRequest(achievement.largeIconPath));
			this.addChild(this._largeIcon);
			
			// if achievement requires additional conditions (win/survive/be top player/etc.),
			// then display star hinting that medal is not 100% guaranteed, but main condition is met
			if (achievement.conditional)
			{
				this._conditionalStarTextField = new TextField();
				this._conditionalStarTextField.mouseEnabled = false;
				this._conditionalStarTextField.antiAliasType = AntiAliasType.NORMAL;
				this._conditionalStarTextField.autoSize = TextFieldAutoSize.LEFT;
				this._conditionalStarTextField.background = false;
				this._conditionalStarTextField.border = false;
				this._conditionalStarTextField.multiline = false;
				this._conditionalStarTextField.selectable = false;
				this._conditionalStarTextField.type = TextFieldType.DYNAMIC;
				this._conditionalStarTextField.wordWrap = true;
				this._conditionalStarTextField.defaultTextFormat = new TextFormat("$FieldFont", 54, 0xFFFF00);
				this._conditionalStarTextField.text = "*";
				this._conditionalStarTextField.x = 0;
				this._conditionalStarTextField.y = -10;
				this.addChild(this._conditionalStarTextField);
			}
			
			// achievement name
			this._achievementNameTextField = new TextField();
			this._achievementNameTextField.mouseEnabled = false;
			this._achievementNameTextField.antiAliasType = AntiAliasType.NORMAL;
			this._achievementNameTextField.autoSize = TextFieldAutoSize.LEFT;
			this._achievementNameTextField.background = false;
			this._achievementNameTextField.border = false;
			this._achievementNameTextField.multiline = false;
			this._achievementNameTextField.selectable = false;
			this._achievementNameTextField.type = TextFieldType.DYNAMIC;
			this._achievementNameTextField.wordWrap = true;
			this._achievementNameTextField.defaultTextFormat = new TextFormat("$FieldFont", 20, 0xFFFFFF);
			this._achievementNameTextField.text = achievement.text;
			this._achievementNameTextField.width = TEXT_WIDTH;
			this._achievementNameTextField.x = ICON_SIZE;
			
			this.addChild(this._achievementNameTextField);
			
			// achievement description
			this._achievementDescriptionTextField = new TextField();
			this._achievementDescriptionTextField.mouseEnabled = false;
			this._achievementDescriptionTextField.antiAliasType = AntiAliasType.NORMAL;
			this._achievementDescriptionTextField.autoSize = TextFieldAutoSize.LEFT;
			this._achievementDescriptionTextField.background = false;
			this._achievementDescriptionTextField.border = false;
			this._achievementDescriptionTextField.multiline = true;
			this._achievementDescriptionTextField.selectable = false;
			this._achievementDescriptionTextField.type = TextFieldType.DYNAMIC;
			this._achievementDescriptionTextField.wordWrap = true;
			this._achievementDescriptionTextField.defaultTextFormat = new TextFormat("$FieldFont", 14, 0xa19c95);
			
			var descriptionExtension:String = "";
			if (achievement.extended)
			{
				if (extended)
				{
					descriptionExtension = "\n" + achievement.descriptionExtendedText;
				}
				else
				{
					descriptionExtension = "\n" + achievement.descriptionStandardText;
				}
			}
			
			this._achievementDescriptionTextField.text = achievement.descriptionText + descriptionExtension;
			this._achievementDescriptionTextField.width = TEXT_WIDTH;
			this._achievementDescriptionTextField.x = ICON_SIZE;
			this._achievementDescriptionTextField.y = this._achievementNameTextField.y + this._achievementNameTextField.height;
			
			this.addChild(this._achievementDescriptionTextField);
			
			// achievement condition
			this._achievementConditionTextField = new TextField();
			this._achievementConditionTextField.mouseEnabled = false;
			this._achievementConditionTextField.antiAliasType = AntiAliasType.NORMAL;
			this._achievementConditionTextField.autoSize = TextFieldAutoSize.LEFT;
			this._achievementConditionTextField.background = false;
			this._achievementConditionTextField.border = false;
			this._achievementConditionTextField.multiline = true;
			this._achievementConditionTextField.selectable = false;
			this._achievementConditionTextField.type = TextFieldType.DYNAMIC;
			this._achievementConditionTextField.wordWrap = true;
			this._achievementConditionTextField.defaultTextFormat = new TextFormat("$FieldFont", 12, 0x6e6862);
			this._achievementConditionTextField.text = achievement.conditionText;
			this._achievementConditionTextField.width = TEXT_WIDTH;
			this._achievementConditionTextField.x = ICON_SIZE;
			this._achievementConditionTextField.y = this._achievementDescriptionTextField.y + this._achievementDescriptionTextField.height + 5;
			
			this.addChild(this._achievementConditionTextField);
			
			this.recalculateBackground();
		}
		
		private function onIconLoadingComplete(event:Event) : void
		{
			this._largeIcon.width = ICON_SIZE;
			this._largeIcon.height = ICON_SIZE;
			this._largeIcon.y = (this.height - this._largeIcon.height) / 2.0;
			
			this._largeIcon.contentLoaderInfo.removeEventListener(Event.COMPLETE, this.onIconLoadingComplete);
			
			this.recalculateBackground();
		}
		
		private function recalculateBackground() : void
		{
			this.graphics.clear();
			this.graphics.lineStyle(1, 0xa19c95)
			this.graphics.beginFill(0x000000, 0.9);
			this.graphics.drawRoundRect(-5, -5, this.width + 10, this.height + 10, 20, 20);
			this.graphics.endFill();
		}
		
		public function disposeState() : void
		{
			this.removeChildren();
			
			this._app = null;
			
			this._largeIcon = null;
			this._conditionalStarTextField = null;
			this._achievementNameTextField = null;
			this._achievementDescriptionTextField = null;
			this._achievementConditionTextField = null;
		}
		
	}

}