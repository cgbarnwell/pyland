#include "python_embed_headers.hpp"

#include <boost/iterator/zip_iterator.hpp>
#include <boost/multi_index/detail/bidir_node_iterator.hpp>
#include <boost/multi_index/detail/ord_index_node.hpp>
#include <boost/python/list.hpp>
#include <boost/range/adaptor/reversed.hpp>
#include <glm/vec2.hpp>
#include <glog/logging.h>
#include <ostream>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

#include "entity.hpp"
#include "engine.hpp"
#include "event_manager.hpp"
#include "game_time.hpp"
#include "gil_safe_future.hpp"
#include "object_manager.hpp"
#include "map_object.hpp"
#include "map_viewer.hpp"

Entity::Entity(glm::vec2 start, std::string name, std::string file_location, int id):
    start(start), id(id), call_number(0) {
        this->name = std::string(name);
        this->file_location = std::string(file_location);
        LOG(INFO) << "invalid: constructor " << this->id;
}

//A dummy function for testing callbacks in python, TODO: once this has been refered to to implement an even-driven callback system, remove this!!! 
void Entity::callback_test(PyObject *callback) {
    boost::python::object boost_callback(boost::python::handle<>(boost::python::borrowed(callback)));
    //GilSafeFuture<void>::execute([boost_callback] (GilSafeFuture<void>) {
    //	PyGILState_STATE state = PyGILState_Ensure();
    //	boost_callback();
    //	PyGILState_Release(state);
    //});
    //EventManager::get_instance().add_event([boost_callback] () {
    //	PyGILState_STATE state = PyGILState_Ensure();
    //	LOG(INFO) << "PP";
    //	boost_callback();
    //	LOG(INFO) << "PPP";
    //	PyGILState_Release(state);
    //	LOG(INFO) << "PPPP";
    //});
    EventManager::get_instance().add_event(boost_callback);
}

void Entity::move(int x, int y) {
    ++call_number;

    auto id = this->id;
    GilSafeFuture<bool>::execute(
        [id, x, y] (GilSafeFuture<bool> walk_succeeded_return) {
            Engine::move_object(id, glm::ivec2(x, y), walk_succeeded_return); //This returns a boolean that says wether the move was succesful or not...
        },
        false
    );
    return;
}

void Entity::move_east(){
    return(move(1, 0));
}

void Entity::move_west(){
    return(move(-1, 0));
}

void Entity::move_north(){
    return(move(0, 1));
}

void Entity::move_south(){
    return(move(0, -1));
}

bool Entity::walkable(int x, int y) {
    ++call_number;

    auto id = this->id;
    return GilSafeFuture<bool>::execute(
        [id, x, y] (GilSafeFuture<bool> walk_succeeded_return) {
            walk_succeeded_return.set(
                // TODO: assert integral
                Engine::walkable(glm::ivec2(Engine::find_object(id)) + glm::ivec2(x, y))
            );
        },
        false
    );

    // TODO (Joshua): Support:
    //
    //     return GilSafeFuture<bool>::execute_get([id, x, y] () {
    //         return Engine::walkable(glm::ivec2(Engine::find_object(id)) + glm::ivec2(x, y));
    //     });
    //
}

void Entity::monologue() {
    auto id = this->id;
    auto name = this->name;
    return GilSafeFuture<void>::execute([id, name] (GilSafeFuture<void>) {
        std::ostringstream stream;

        auto where(Engine::find_object(id));
        stream << "I am " << name << " and "
               << "I am standing at " << where.x << ", " << where.y << "!";

        Engine::print_dialogue(name, stream.str());
    });
}

void Entity::focus() {
    auto id = this->id;
    return GilSafeFuture<void>::execute([id] (GilSafeFuture<void>) {
        MapViewer *map_viewer = Engine::get_map_viewer();
        map_viewer->set_map_focus_object(id);
    });
}

std::string Entity::get_name() { //TODO: Analyse wether it would be best to get this information from the object instance, instead of from the information copied into this instance. (and then not have that information here)
    std::string name = this->name;
    return GilSafeFuture<std::string>::execute([name] (GilSafeFuture<std::string> instructions_return) {
            instructions_return.set(name);
    });
}

std::string Entity::get_location() {
    std::string file_location = this->file_location;
    return GilSafeFuture<std::string>::execute([file_location] (GilSafeFuture<std::string> instructions_return) {
            instructions_return.set(file_location);
    });
}

std::string Entity::get_instructions() {
    auto id(this->id);
    return GilSafeFuture<std::string>::execute([id] (GilSafeFuture<std::string> instructions_return) {
        auto sprite(ObjectManager::get_instance().get_object<MapObject>(id));

        if (sprite) {
            //instructions_return.set(sprite->get_instructions()); TODO: BLEH work out what this did
        }
        else {
            instructions_return.set("Try thinking about the problem in a different way.");
        }
    });
}

// Not thread safe for efficiency reasons...
void Entity::py_print_debug(std::string text) {
    LOG(INFO) << text;
}

void Entity::py_print_dialogue(std::string text) {
    auto name = this->name;
    return GilSafeFuture<void>::execute([name, text] (GilSafeFuture<void>) {
        Engine::print_dialogue(name, text);
    });
}

void Entity::__set_game_speed(float game_seconds_per_real_second) {
    return GilSafeFuture<void>::execute([game_seconds_per_real_second] (GilSafeFuture<void>) {
        EventManager::get_instance().time.set_game_seconds_per_real_second(game_seconds_per_real_second);
    });
}

void Entity::py_update_status(std::string status){
    auto id(this->id);
    return GilSafeFuture<void>::execute([id, status] (GilSafeFuture<void>) {
        //Engine::update_status(id, status); TODO: BLEH work out what this did 
    });
}

// This is way too complecated...
//
// but I blame C++
py::list Entity::get_retrace_steps() {
    auto id(this->id);
    return GilSafeFuture<py::list>::execute([id] (GilSafeFuture<py::list> retrace_steps_return) {
        py::list retrace_steps;

        auto object(ObjectManager::get_instance().get_object<MapObject>(id));
        auto &positions(object->get_positions());

        auto zipped_locations_begin(boost::make_zip_iterator(boost::make_tuple(
            std::next(positions.get<insertion_order>().rbegin()), positions.get<insertion_order>().rbegin()
        )));
        auto zipped_locations_end(boost::make_zip_iterator(boost::make_tuple(
            positions.get<insertion_order>().rend(), std::prev(positions.get<insertion_order>().rend())
        )));

        for (auto pair=zipped_locations_begin; pair != zipped_locations_end; ++pair) {
            glm::vec2 start(pair->get<0>());
            glm::vec2 end  (pair->get<1>());
            auto reverse_change(start - end);

            retrace_steps.append(py::make_tuple(
                py::api::object(float(reverse_change.x)),
                py::api::object(float(reverse_change.y))
            ));
        }

        retrace_steps_return.set(retrace_steps);
    });
}

py::object Entity::read_message() {
    auto id(this->id);
    return GilSafeFuture<py::object>::execute([id] (GilSafeFuture<py::object> read_message_return) {
        auto object(ObjectManager::get_instance().get_object<MapObject>(id));
        auto *challenge(object->get_challenge());

        if (challenge) {
            read_message_return.set(challenge->read_message(id));
        }
        else {
            read_message_return.set(py::object());
        }
    });
}
