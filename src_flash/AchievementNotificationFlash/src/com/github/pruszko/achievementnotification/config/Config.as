package com.github.pruszko.achievementnotification.config
{
	import com.github.pruszko.achievementnotification.utils.Disposable;
	
	public class Config implements Disposable
	{
		
		public static const DISPLAY_MODE_COMPACT:String = "compact";
		public static const DISPLAY_MODE_DETAILED:String = "detailed";
		
		private var _displayMode:String = DISPLAY_MODE_DETAILED;
		private var _verticalPosition:Number = 0.8;
		
		private var _firstDisplayTime:Number = 5.0;
		private var _consecutiveDisplayTime:Number = 3.0;
		
		public function Config() 
		{
			super();
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._displayMode = serializedSection["display-mode"];
			this._verticalPosition = serializedSection["vertical-position"];
			this._firstDisplayTime = serializedSection["first-display-time"];
			this._consecutiveDisplayTime = serializedSection["consecutive-display-time"];
		}
		
		public function disposeState() : void
		{
			
		}
		
		public function get displayMode() : String
		{
			return this._displayMode;
		}
		
		public function get verticalPosition() : Number
		{
			return this._verticalPosition;
		}
		
		public function get firstDisplayTime() : Number
		{
			return this._firstDisplayTime;
		}
		
		public function get consecutiveDisplayTime() : Number
		{
			return this._consecutiveDisplayTime;
		}
		
	}

}