package com.github.pruszko.achievementnotification.queue
{
	import com.github.pruszko.achievementnotification.AchievementNotificationFlash;
	import com.github.pruszko.achievementnotification.achievements.AchievementNotification;
	import com.github.pruszko.achievementnotification.config.Config;
	import com.github.pruszko.achievementnotification.utils.Disposable;
	import com.github.pruszko.achievementnotification.queue.Transition;
	import flash.display.DisplayObject;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.events.TimerEvent;
	
	public class NotificationBar extends Sprite implements Disposable
	{
		
		private static const FADE_IN_TIME:int = 500;
		private static const FADE_OUT_TIME:int = 500;
		
		// code here will look like garbage, because
		// writing a state machine is always ... not so easy
		//
		// and doing it in abandoned language doesn't help
		private static const STATE_READY:int = 0;
		private static const STATE_FADING_IN:int = 1;
		private static const STATE_DISPLAYING:int = 2;
		private static const STATE_FADING_OUT:int = 3;
		
		private var _app:AchievementNotificationFlash;
		
		private var _currentState:int = STATE_READY;
		
		private var _currentTransition:Transition = null;
		private var _isMouseHovering:Boolean = false;
		
		public function NotificationBar(app:AchievementNotificationFlash) 
		{
			super();
			this._app = app;
		}
		
		public function addNotification(notification:AchievementNotification) : void
		{
			notification.alpha = 0.0;
			this.addChildAt(notification, 0);
			
			if (this._currentState == STATE_READY)
			{
				notification.displayTime = this.config.firstDisplayTime;
				
				this._currentState = STATE_FADING_IN;
				
				this.setupTransition();
				this.currentTransition.transition(1.0, FADE_IN_TIME);
				this.startMouseListening();
			}
			else
			{
				notification.displayTime = this.config.consecutiveDisplayTime;
			}
		}
		
		public function onTransitionFinish() : void
		{
			if (this._currentState == STATE_FADING_IN)
			{
				this._currentState = STATE_DISPLAYING;
				
				if (this._isMouseHovering)
				{
					this.currentTransition.stop();
				}
				else
				{
					this.currentTransition.transition(1.0, int(this.currentNotification.displayTime * 1000.0));
				}
			}
			else if (this._currentState == STATE_DISPLAYING)
			{
				this._currentState = STATE_FADING_OUT;
				this.currentTransition.transition(0.0, FADE_OUT_TIME);
			}
			else if (this._currentState == STATE_FADING_OUT)
			{
				this.cancelMouseListening();
				this.disposeCurrentTransition();
				this.disposeCurrentNotification();
				
				if (this.numChildren > 0)
				{
					this._currentState = STATE_FADING_IN;
					
					this.setupTransition();
					this.currentTransition.transition(1.0, FADE_IN_TIME);
					this.startMouseListening();
				}
				else
				{
					this._currentState = STATE_READY;
				}
			}
		}
		
		private function startMouseListening() : void
		{
			this.addEventListener(MouseEvent.MOUSE_OVER, this.onMouseOver);
			this.addEventListener(MouseEvent.MOUSE_OUT, this.onMouseOut);
			this.addEventListener(MouseEvent.CLICK, this.onMouseClick);
		}
		
		private function cancelMouseListening() : void
		{
			this.removeEventListener(MouseEvent.MOUSE_OVER, this.onMouseOver);
			this.removeEventListener(MouseEvent.MOUSE_OUT, this.onMouseOut);
			this.removeEventListener(MouseEvent.CLICK, this.onMouseClick);
		}
		
		private function onMouseOver(mouseEvent:MouseEvent) : void
		{
			this._isMouseHovering = true;
			
			if (this._currentState == STATE_DISPLAYING)
			{
				this.currentTransition.stop();
			}
			else if (this._currentState == STATE_FADING_OUT)
			{
				this._currentState = STATE_FADING_IN;
				this.currentTransition.transition(1.0, FADE_IN_TIME);
			}
		}
		
		private function onMouseOut(mouseEvent:MouseEvent) : void
		{
			this._isMouseHovering = false;
			
			if (this._currentState == STATE_DISPLAYING)
			{
				this._currentTransition.transition(1.0, int(this.config.consecutiveDisplayTime * 1000.0));
			}
		}
		
		private function onMouseClick(mouseEvent:MouseEvent) : void
		{
			this._currentState = STATE_FADING_OUT;
			this.currentTransition.stop();
			
			this.onTransitionFinish();
			
			if (this.numChildren == 0)
			{
				// if clicked notification was last element in notification bar
				// then "mouse out" event WON'T be dispatched
				// because we haven't moved our mouse out of notification bar
				// but instead notification bar "collapsed" to 0 width/height, escaping our mouse
				//
				// this would cause next achievement notification be permanently displayed
				// until we move our mouse over and out at notification again
				// due to check in onTransitionFinish() method
				//
				// just force set that flag when notification bar is empty and everything is fine
				this._isMouseHovering = false;
			}
		}
		
		private function get currentNotification() : AchievementNotification
		{
			return this.numChildren > 0 ? (this.getChildAt(this.numChildren - 1) as AchievementNotification) : null;
		}
		
		private function disposeCurrentNotification() : void
		{
			this.currentNotification.disposeState();
			this.removeChildAt(this.numChildren - 1);
		}
		
		private function setupTransition() : void
		{
			this._currentTransition = new Transition(this.currentNotification, "alpha");
			this._currentTransition.addEventListener(TimerEvent.TIMER_COMPLETE, this.onTransitionFinish);
		}
		
		private function get currentTransition() : Transition
		{
			return this._currentTransition;
		}
		
		private function get config() : Config
		{
			return this._app.config;
		}
		
		private function disposeCurrentTransition() : void
		{
			this._currentTransition.removeEventListener(TimerEvent.TIMER_COMPLETE, this.onTransitionFinish);
			this._currentTransition.disposeState();
			this._currentTransition = null;
		}
		
		public function disposeState() : void
		{
			this.cancelMouseListening();
			if (this._currentTransition != null)
			{
				this.disposeCurrentTransition();
			}
			
			while (this.numChildren > 0)
			{
				this.disposeCurrentNotification();
			}
		}
		
	}

}