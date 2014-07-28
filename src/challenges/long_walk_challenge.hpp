#ifndef LONG_WALK_CHALLENGE_H
#define LONG_WALK_CHALLENGE_H

#include <string>
#include <vector>

#include "challenge.hpp"
#include "dispatcher.hpp"
#include "map.hpp"

class LongWalkChallenge : public Challenge {
    public:
        LongWalkChallenge(std::string editor);

        virtual void start();
        virtual void finish();

    private:
        std::vector<Map::Blocker> wall_path_medium_blockers;
        std::vector<Map::Blocker> wall_path_long_blockers;
        std::vector<PositionDispatcher<int>::CallbackID> room_exit_first_callback;
};

#endif