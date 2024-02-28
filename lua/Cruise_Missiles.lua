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
		target_vector = Vector3.Normalize(target_position - missile_position) -- Normalized vector to target
        
        velocity_error = target_velocity - missile_velocity -- Diiference in absolute velocities
        position_error = target_position - missile_position -- Difference in position
        
        I:Log(tostring(Vector3.Magnitude(velocity_error)).."     "..tostring(Vector3.Magnitude(position_error)))
    
		point = missile_position + target_velocity/5 + 10*position_error/Vector3.Magnitude(velocity_error)

        -- Generate new target point, matching velocity and moving closer gradually
		-- point = missile_position + 0.9*velocity_error + 0.1*position_error*Vector3.Magnitude(position_error)

		I:SetLuaControlledMissileAimPoint(t, m, point.x, point.y, point.z)
		end
	end
end