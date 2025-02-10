package com.github.pruszko.achievementnotification.config
{
	import com.github.pruszko.achievementnotification.utils.Disposable;
	
	public class Config implements Disposable
	{
		
		private var _firstDisplayTime:Number = 5.0;
		private var _consecutiveDisplayTime:Number = 3.0;
		
		public function Config() 
		{
			super();
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._firstDisplayTime = serializedSection["first-display-time"];
			this._consecutiveDisplayTime = serializedSection["consecutive-display-time"];
		}
		
		public function disposeState() : void
		{
			
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