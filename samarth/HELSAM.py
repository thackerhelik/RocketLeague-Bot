from tools import  *
from objects import *
from routines import *

class HELSAM(GoslingAgent):
	def run(agent):

		close = (agent.me.location - agent.ball.location).magnitude() < 2000
		have_boost = agent.me.boost > 20
		
		my_goal_to_ball, my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
		my_goal_to_me = agent.me.location - agent.friend_goal.location
		my_distance = my_goal_to_ball.dot(my_goal_to_me)

		foe_goal_to_ball, foe_ball_distance = (agent.ball.location - agent.foe_goal.location).normalize(True)
		foe_goal_to_foe = agent.foes[0].location - agent.foe_goal.location
		foe_distance = foe_goal_to_ball.dot(foe_goal_to_foe) 


		me_onside = my_distance - 200 < my_ball_distance
		foe_onside = foe_distance - 200 < foe_ball_distance


		if agent.team == 0:
			agent.debug_stack()
			agent.line(agent.friend_goal.location, agent.ball.location, [255, 255, 255])
			my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
			agent.line(my_point - Vector3(0, 0, 100), my_point + Vector3(0, 0, 100), [0, 255, 0])
			print(me_onside, foe_onside, close)

		return_to_goal = False

		if len(agent.stack) < 1:
			if agent.kickoff_flag:
				agent.push(kickoff())
			elif (close and me_onside) or (not foe_onside and me_onside):
				left_field = Vector3(4200*-side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
				right_field = Vector3(4200*side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
				targets = {"goal": (agent.foe_goal.left_post, agent.foe_goal.right_post), "upfield": (left_field, right_field)}
				shots = find_hits(agent, targets)
				if len(shots["goal"]) > 0:
					agent.push(shots["goal"][0])
				elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
					agent.push(shots["upfield"][0])
				else:
					return_to_goal = True
			elif not me_onside and not have_boost:
				boosts = [boost for boost in agent.boosts if boost.large and boost.active and abs(agent.friend_goal.location.y - boost.location.y) - 200 < abs(agent.friend_goal.location.y)]
				if len(boosts) > 0:
					closest = boosts[0]
					for boost in boosts:
						if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
							closest = boost
					agent.push(goto_boost(closest, agent.friend_goal.location))
				else:
					return_to_goal = True
			else:
				agent.push(short_shot(agent.foe_goal.location))

		if return_to_goal == True:
			relative_target = agent.friend_goal.location - agent.me.location
			angles = defaultPD(agent, agent.me.local(relative_target))
			defaultThrottle(agent, 2300)
			if abs(angles[1]) > 0.5 or agent.me.airborne: #radians
				agent.controller.boost = False
			if abs(angles[1]) > 2.8:
				agent.controller.handbrake = True



			# agent.push(wavedash())
			# large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
			# closest = large_boosts[0]
			# closest_distance = (large_boosts[0].location - agent.me.location).magnitude()

			# for item in large_boosts:
			# 	item_distance = (item.location- agent.me.location).magnitude()
			# 	if item_distance < closest_distance:
			# 		closest = item
			# 		closest_distance = item_distance

			# agent.push(goto_boost(closest))

			# agent.push(short_shot(agent.foe_goal.location))

			# relative_target = agent.foes[0].location - agent.me.location
			# local_target = agent.me.local(relative_target)
			# agent.push(flip(local_target))

			# targets = {"goal": (agent.foe_goal.left_post, agent.foe_goal.right_post)}
			# shots = find_hits(agent, targets)
			# if len(shots["goal"]) > 0:
			# 	agent.push(shots["goal"][0])
			# else:
			# 	relative = agent.ball.location - agent.me.location
			# 	defaultPD(agent, agent.me.local(relative))
			# 	defaultThrottle(agent, 1410)


			