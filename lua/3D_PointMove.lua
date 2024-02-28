function Update(I)
	self_position = I:GetConstructPosition()
	self_velocity = I:GetVelocityVector()
    self_angle = I:GetConstructForwardVector()
	
	target_position = I:GetTargetInfo(0, 0).AimPointPosition
	target_velocity = I:GetTargetInfo(0, 0).Velocity	
    

    target_vector = Vector3.Normalize(target_position - self_position) -- Normalized vector to target
    
    I:GetConstructForwardVector()
    I:GetConstructRightVector()
    I:GetConstructUpVector()
end



function XZDistance(p1, p2)
	return math.sqrt((p1.x - p2.x)^2 + (p1.z - p2.z)^2)
end