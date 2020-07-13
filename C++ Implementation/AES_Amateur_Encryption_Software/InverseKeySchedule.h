#pragma once
#include "KeySchedule.h"
class InverseKeySchedule :
    public KeySchedule
{
public: 
    InverseKeySchedule(const std::vector<uint8_t>& key);
    virtual uint32_t next();
    virtual void reset();
private:
    int blockCounter;
    int startIndex();
};

