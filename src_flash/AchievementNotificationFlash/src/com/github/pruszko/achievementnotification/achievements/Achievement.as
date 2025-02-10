package com.github.pruszko.achievementnotification.achievements
{
	import com.github.pruszko.achievementnotification.utils.Disposable;
	
	public class Achievement implements Disposable
	{
		
		private var _key:String;
		private var _extended:Boolean;
		private var _conditional:Boolean;
		
		private var _text:String;
		private var _descriptionText:String;
		private var _descriptionStandardText:String;
		private var _descriptionExtendedText:String;
		private var _conditionText:String;
		
		private var _largeIconPath:String;
		
		public function Achievement(serializedAchievement:Object)
		{
			this._key = serializedAchievement["key"];
			this._extended = serializedAchievement["extended"];
			this._conditional = serializedAchievement["conditional"];
			
			this._text = serializedAchievement["text"];
			this._descriptionText = serializedAchievement["descriptionText"];
			this._descriptionStandardText = serializedAchievement["descriptionStandardText"];
			this._descriptionExtendedText = serializedAchievement["descriptionExtendedText"];
			this._conditionText = serializedAchievement["conditionText"];
			
			this._largeIconPath = serializedAchievement["largeIconPath"];
		}
		
		public function disposeState() : void
		{
			
		}
		
		public function get key() : String
		{
			return this._key;
		}
		
		public function get extended() : Boolean
		{
			return this._extended;
		}
		
		public function get conditional() : Boolean
		{
			return this._conditional;
		}
		
		public function get text() : String
		{
			return this._text;
		}
		
		public function get descriptionText() : String
		{
			return this._descriptionText;
		}
		
		public function get descriptionStandardText() : String
		{
			return this._descriptionStandardText;
		}
		
		public function get descriptionExtendedText() : String
		{
			return this._descriptionExtendedText;
		}
		
		public function get conditionText() : String
		{
			return this._conditionText;
		}
		
		public function get largeIconPath() : String
		{
			return this._largeIconPath;
		}
		
	}

}