local loginField = dcFile:getClassByName("TTGameServicesManager"):getFieldByName("login"):getNumber()

function receiveDatagram(client, di)
    local message = di:readUint16()
    local state = client:userTable()
    if not state.hello then
        if message ~= 1 then
            client:sendDisconnect(106, "Expected hello")
            return
        end
        local hash, version = di:readUint32(), di:readString()
        if hash ~= DC_HASH or version ~= SERVER_VERSION then
            client:sendDisconnect(125, "Client version or DC hash mismatch")
            return
        end
        state.hello = true
        client:userTable(state)
        local reply = datagram:new()
        reply:addUint16(2)
        client:sendDatagram(reply)
    elseif message == 3 then
        client:handleDisconnect()
    elseif message == 5 then
        client:handleHeartbeat()
    elseif message == 120 then
        local object, field = di:readUint32(), di:readUint16()
        if not client:authenticated() and (object ~= 4670 or field ~= loginField) then
            client:sendDisconnect(113, "Login required")
            return
        end
        local update = datagram:new()
        update:addUint32(object)
        update:addUint16(field)
        update:addData(di:readRemainder())
        client:handleUpdateField(datagramiterator.new(update))
    elseif not client:authenticated() then
        client:sendDisconnect(113, "Login required")
    elseif message == 200 or message == 201 then
        local context, handle, parent = di:readUint32(), di:readUint16(), di:readUint32()
        local count = 1
        if message == 201 then count = di:readUint16() end
        local zones = {}
        for i = 1, count do zones[i] = di:readUint32() end
        client:handleAddInterest(handle, context, parent, zones)
    elseif message == 203 then
        local context, handle = di:readUint32(), di:readUint16()
        client:handleRemoveInterest(handle, context)
    elseif message == 140 then
        client:setLocation(di)
    else
        client:sendDisconnect(108, "Unsupported client message")
    end
    if di:getRemainingSize() ~= 0 then
        client:sendDisconnect(109, "Unexpected data after client message")
    end
end
