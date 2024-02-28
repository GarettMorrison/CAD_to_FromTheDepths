-- Yoinked from u/wrigh516 on Reddit
-- https://www.reddit.com/r/FromTheDepths/comments/lh4jnd/comparing_lua_missile_guidance_code_and/
-- https://pastebin.com/Yd3uxiEE

function Update(I)
	self_position = I:GetConstructPosition()
	target_position = I:GetTargetInfo(0, 0).AimPointPosition
	target_velocity = I:GetTargetInfo(0, 0).Velocity

	for t = 0, I:GetLuaTransceiverCount() do
		for m = 0, I:GetLuaControlledMissileCount(t) - 1 do
		missile_position = I:GetLuaControlledMissileInfo(t, m).Position
		missile_velocity = I:GetLuaControlledMissileInfo(t, m).Velocity
		missile_speed = Vector3.Magnitude(missile_velocity)

		target_distance = Vector3.Distance(target_position, missile_position)
		target_vector = Vector3.Normalize(target_position - missile_position)

		relative_speed = missile_speed - Vector3.Dot(target_vector, target_velocity)
		prediction = target_velocity*target_distance/relative_speed

		intercept = target_position + prediction
		intercept_vector = Vector3.Normalize(intercept - missile_position)  

		point = missile_position + intercept_vector*missile_speed

		target_xzdistance = XZDistance(target_position, missile_position)

		-- if (target_xzdistance > 300) then
		--   point.y = 500
		-- end
		
		-- point = target_position

		I:SetLuaControlledMissileAimPoint(t, m, point.x, point.y, point.z)
		end
	end
end
   
   
   
function XZDistance(p1, p2)
	return math.sqrt((p1.x - p2.x)^2 + (p1.z - p2.z)^2)
end





function ProgressToTarget(sp, tp, mp)
	distance = Vector3.Distance(tp, sp)
	vector = Vector3.Normalize(tp - sp)
	progress = Vector3.Dot(vector, mp - sp)/distance
	if (progress < 0) then
		return 0
	elseif (progress > 1) then
		return 1
	else
		return progress
	end
end