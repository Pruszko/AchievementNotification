package com.github.pruszko.achievementnotification.queue
{
	import com.github.pruszko.achievementnotification.queue.NotificationBar;
	import com.github.pruszko.achievementnotification.utils.Disposable;
	import flash.display.DisplayObject;
	import flash.events.EventDispatcher;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	
	public class Transition extends EventDispatcher implements Disposable
	{
		
		private static const STEPS_PER_SECOND:int = 20;
		private static const STEPS_INTERVAL:int = int(1000 / STEPS_PER_SECOND);
		
		private var _obj:Object;
		private var _property:String;
		
		private var _timer:Timer = null;
		
		private var _from:Number = 0.0;
		private var _to:Number = 0.0;

		public function Transition(obj:Object, property:String)
		{
			super();
			
			this._obj = obj;
			this._property = property;
		}
		
		public function transition(to:Number, timeMillis:int) : void
		{
			this._from = this._obj[this._property];
			this._to = to;
			
			if (this._timer != null)
			{
				this.disposeTimer();
			}
			
			var totalSteps:int = int(timeMillis * STEPS_PER_SECOND / 1000);
			
			this._timer = new Timer(STEPS_INTERVAL, totalSteps);
			this._timer.addEventListener(TimerEvent.TIMER, this.onTimerTick)
			this._timer.addEventListener(TimerEvent.TIMER_COMPLETE, this.onTimerComplete);
			this._timer.start();
		}
		
		public function stop() : void
		{
			if (this._timer != null)
			{
				this.disposeTimer();
			}
		}
		
		private function onTimerTick() : void
		{
			var prop:Number = this._timer.currentCount / this._timer.repeatCount;
			this._obj[this._property] = this._from + (this._to * prop) - (this._from * prop)
		}
		
		private function onTimerComplete(timerEvent:TimerEvent) : void
		{
			this.disposeTimer();
			
			this.dispatchEvent(timerEvent);
		}
		
		private function disposeTimer() : void
		{
			this._timer.stop();
			this._timer.removeEventListener(TimerEvent.TIMER, this.onTimerTick);
			this._timer.removeEventListener(TimerEvent.TIMER_COMPLETE, this.onTimerComplete);
			this._timer = null;
		}
		
		public function disposeState() : void
		{
			this._obj = null;
			this._property = null;
			
			if (this._timer != null)
			{
				this.disposeTimer();
			}
		}
		
	}

}