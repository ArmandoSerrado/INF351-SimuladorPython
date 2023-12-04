/// @file    RGBCalibrate.ino
/// @brief   Use this to determine what the RGB ordering for your LEDs should be
/// @example RGBCalibrate.ino



#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <Fonts/FreeMonoBoldOblique12pt7b.h>
#include <Fonts/Picopixel.h>

const char* ssid = "iPhone";
const char* password = "armando123";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// #include <LiquidCrystal.h>

// // Define as conexões e cria o objeto para acesso
// const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
// const int backLight = 10;
// LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


#include "FastLED.h"
#include "vector"
#include "string.h"

#define NUM_LEDS 64
#define DATA_PIN 2

CRGB leds[NUM_LEDS];

#define TILEGRID_LENGHT 43
#define TILEGRID_HEIGHT 36

int TILEGRID [TILEGRID_HEIGHT][TILEGRID_LENGHT] = 
      {{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
       {1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
       {1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
       {1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1},
       {1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
       {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}};

#define GROUND_TILE 0
#define WALL_TILE 1
#define DOOR_TILE 2
#define OPEN_DOOR_TILE 3

#define K_UP 1
#define K_DOWN 2
#define K_LEFT 3
#define K_RIGHT 4
#define K_r 5
#define K_p 6

// Limites para detecção das teclas, em ordem crescente
// struct {
//   int limit;
//   int key;
// } lcd_keys[] = {
//   {   50, K_RIGHT },
//   {  150, K_UP },
//   {  300, K_DOWN },
//   {  500, K_LEFT },
//   {  750, K_r },
//   { 1024, 0 }  // nenhuma tecla apertada
// };


Adafruit_NeoMatrix *matrix = new Adafruit_NeoMatrix(8, 8, DATA_PIN,
    NEO_MATRIX_BOTTOM     + NEO_MATRIX_LEFT +
    NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG,
    NEO_GRB            + NEO_KHZ800);

class Vector2D  {
public:
  Vector2D(int x = 0, int y = 0) : x(x), y(y) {}
  Vector2D(const Vector2D& other) : x(other.x), y(other.y) {}
  int x, y;

  Vector2D& operator=(const Vector2D& other) {
    this->x = other.x;
    this->y = other.y;
    return *this;
  }

  Vector2D operator+(const Vector2D& other) const {
    Vector2D temp = *this;
    temp.x = temp.x + other.x;
    temp.y = temp.y + other.y;
    return temp;
  }

  Vector2D operator-(const Vector2D& other) const {
    Vector2D temp = *this;
    temp.x = temp.x - other.x;
    temp.y = temp.y - other.y;
    return temp;
  }

  Vector2D operator*(int k) const {
    Vector2D temp = *this;
    temp.x = temp.x * k;
    temp.y = temp.y * k;
    return temp;
  }

  Vector2D operator/(int k) const {
    Vector2D temp = *this;
    temp.x = temp.x / k;
    temp.y = temp.y / k;
    return temp;
  }

  bool operator==(const Vector2D& other) const {
    return (this->x == other.x && this->y == other.y);
  }

};

void led(int x, int y, CRGB color = CRGB::White) {
  if(y%2 == 0)
    leds[x + (y*8)] = color;
  else 
    leds[(7 - x) + (y*8)] = color;
}
void led(const Vector2D& position, CRGB color = CRGB::White) {
  led(position.x, position.y, color);
}

void fill(CRGB color) {
  for (int i = 0; i < 8; i++)
    for (int j = 0; j < 8; j++)
      led(i ,j ,color);
}


class Entity{
public:
  Entity() {
    type = "ENTITY";
    color = CRGB::White;
    is_alive = true;
  }
  virtual void process() {}
  virtual void process_input() {}

  const Vector2D& get_position() const { return position;}
  void set_position(const Vector2D& position) { this->position = position;}

  const String& get_type() const { return type;}
  void set_type(const String& type) { this->type = type;}

  const CRGB& get_color() const {return color;}
  void set_color(const CRGB& color) {this->color = color;}

  bool is_colliding(const Entity& other) const{
    return (other.is_alive && this->is_alive && other.position == this->position);
  }

  bool is_alive;
private:
  Vector2D position;
  String type;
  CRGB color;
};

class Mobile : public Entity {
public:
  Mobile() : direction(0,0) {}
  ~Mobile() {}

  virtual void process() {
    Entity::process();
    process_physics();
  }
  virtual void process_input(int event) {}
  virtual void process_physics() {
    move_and_collide();
  }

  const Vector2D& get_direction() const {return direction;}
  void set_direction(const Vector2D& direction) { this->direction = direction;}

  virtual void move_and_collide() {
    if (!will_collide())
      set_position(get_position() + get_direction());
  }
  bool will_collide() const {
    return (front_tile() != GROUND_TILE &&
            front_tile() != OPEN_DOOR_TILE);
  }

  int front_tile() const {
    Vector2D front = get_position() + get_direction();
    if (front.x < 0 || front.y < 0 || front.x > TILEGRID_LENGHT || front.y > TILEGRID_HEIGHT)
      return 1;
    else
      return TILEGRID[front.y][front.x];
  }
  int self_tile() const {
    return TILEGRID[get_position().y][get_position().x];
  }

  Vector2D front() const {
    return get_position() + get_direction();
  }

private:
  Vector2D direction;
};

class Enemy : public Mobile {
public:
  Enemy(const Vector2D& position) 
  : cooldown(0), last_time(0), current_time(0) {
    this->set_type("ENEMY");
    this->set_color(CRGB::Red);
    this->set_position(position);
  }
  ~Enemy() {}

  virtual void process() {
    current_time = millis();
    if (current_time - last_time > cooldown) {
      last_time = millis();
      Mobile::process();
    }
  }

  int get_cooldown() const { return cooldown;}
  void set_cooldown(int cooldown) {this->cooldown = cooldown;}

private:
  int cooldown;
  int last_time;
  int current_time;
};

std::vector<std::unique_ptr<Enemy>> ENEMIES;

class Enemy_SidetoSide : public Enemy {
public:
  Enemy_SidetoSide(const Vector2D& position, const Vector2D& direction, int cooldown = 1000) 
  : Enemy(position) {
    this->set_direction(direction);
    this->set_cooldown(cooldown);
  }
  ~Enemy_SidetoSide() {}

  virtual void process_physics() {
    Enemy::process_physics();
    if (will_collide())
      set_direction(get_direction() * (-1));
  }
};

class Bullet : public Enemy {
public:
  Bullet(const Vector2D& position, const Vector2D& direction, int cooldown = 200, const CRGB& color = CRGB::Pink) 
  : Enemy(position) {
    this->set_direction(direction);
    this->set_cooldown(cooldown);
    this->set_color(color);
  }
  ~Bullet() {}

  void move_and_collide() {
    if (!will_collide())  
      set_position(get_position() + get_direction());
    else // Projectile hit the wall
      this->is_alive = false;
  }
};

class Cannon : public Enemy {
public:
  Cannon(const Vector2D& position, const Vector2D& direction, int cooldown = 1000) 
  : Enemy(position) {
    this->set_direction(direction);
    this->set_cooldown(cooldown);
  }
  ~Cannon() {}

  void process_physics() {
    ENEMIES.push_back(std::make_unique<Bullet>(get_position(), get_direction(), 200));
  }
};

class Item : public Entity {
public:
  Item(const Vector2D& position = Vector2D(0,0), const String& type = "NONE", const CRGB& color = CRGB::White) {
    this->set_position(position);
    this->set_type(type);
    this->set_color(color);
  }
  ~Item() {}

};

std::vector<std::unique_ptr<Item>> ITEMS;

class Player : public Mobile {
public:
  Player() 
  : keys_collected(0), died(false) {
    this->set_color(CRGB::Blue);
  }
  ~Player() {}

  void reset() {
    is_alive = true;
    died = false;
    set_color(CRGB::Blue);
    keys_collected = 0;
  }

  void process() {
    Mobile::process();

    if (!is_alive && !died) {
      died = true;
      set_color(CRGB(0,0,10));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(1,1), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(1,0), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(1,-1), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(-1,1), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(-1,0), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(-1,-1), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(0,1), 200, CRGB::Blue));
      ENEMIES.push_back(std::make_unique<Bullet>(get_position(), Vector2D(0,-1), 200, CRGB::Blue));
    }
  }

  void process_input(int event) {
    Mobile::process_input(event);

    if (is_alive) {
      if (event == K_UP)
        set_direction(Vector2D(0,1));
      else if (event == K_DOWN)
        set_direction(Vector2D(0,-1));
      else if (event == K_LEFT)
        set_direction(Vector2D(-1,0));
      else if (event == K_RIGHT)
        set_direction(Vector2D(1,0));
    }
  }

  void process_physics() {
    if (!is_alive) return;

    Mobile::process_physics();

    // Opens door
    if (front_tile() == DOOR_TILE && keys_collected > 0) {
      keys_collected--;
      TILEGRID[front().y][front().x] = OPEN_DOOR_TILE;
    }

    set_direction(Vector2D(0,0)); // Stop player after moving

    // Collide with item
    for (auto& item : ITEMS)
      if (item->get_type() == "KEY" && is_colliding(*item)) {
        item->is_alive = false;
        keys_collected++;
      } else if(item->get_type() == "GOAL" && is_colliding(*item))
        item->is_alive = false;

    // Collide with enemy
    for (auto& enemy : ENEMIES) 
      if (is_colliding(*enemy))
        this->is_alive = false;
  }

private:
  int keys_collected;
  bool died;
};


class Camera : public Entity {
public:
  Camera(const Vector2D& projection, const Vector2D& position) {
    this->projection = projection;
    this->set_position(position);
  }
  ~Camera() {}

  void process() {
    Entity::process();
    this->view_position = get_position() - this->projection/2;
    constrain_view();
  }

  const Vector2D& get_viewposition() const { return this->view_position; }
  const Vector2D& get_projection() const { return this->projection; } 


private:
  Vector2D projection, view_position;

  void constrain_view() {
    Vector2D temp_position = this->view_position;
    if (temp_position.x < 0)
      temp_position.x = 0;
    else if (temp_position.x + this->projection.x > TILEGRID_LENGHT)
      temp_position.x = TILEGRID_LENGHT - this->projection.x;

    if (temp_position.y < 0)
      temp_position.y = 0;
    else if (temp_position.y + this->projection.y > TILEGRID_HEIGHT)
      temp_position.y = TILEGRID_HEIGHT - this->projection.y;

    this->view_position = temp_position;
  }

};

class Event {
public:
  Event() {}
  ~Event() {}

  std::vector<int> get() {
    std::vector<int> tmp_events = event;
    event.clear();
    return tmp_events;
  }

  void add(int event) {
    this->event.push_back(event);
  }

private:
  std::vector<int> event;

};

class Menu {
public:
  Menu() : current_index(-1) {}
  ~Menu() {}

  void add_item(const String& text) {
    current_index++;
    menu.push_back(std::vector<String>());
    add_subitem(text);
  }
  void add_subitem(const String& text) {
    menu[current_index].push_back(text);
  }

  void move(const Vector2D& direction) {
    cursor_x = 3;
    if (direction.y != 0)
      this->position.x = 0;

    this->position = direction + this->position;
    if(position.y < 0)
      position.y = 0;
    else if(position.y >= menu.size())
      position.y = menu.size() - 1;

    if(position.x < 0)
      position.x = 0;
    else if(position.x >= menu[position.y].size())
      position.x = menu[position.y].size() - 1;
    
  }

  void render() {
    if (menu.size() == 0) return;

    matrix->fillScreen(50);
    matrix->setCursor(cursor_x, 5);
    matrix->print(menu[position.y][position.x]);
    matrix->setTextColor( matrix->Color(255, 255, 0) );

    if(--cursor_x < -25)
      cursor_x = matrix->width();
    matrix->show();
  }

  const String& get_item() const {
    return menu[position.y][position.x];
  }

private:
  std::vector<std::vector<String>> menu;
  int current_index;
  Vector2D position;
  
  int cursor_x = 3;
};

class Game {
public:
  Game() : camera(Vector2D(8,8), Vector2D(0,0)) {
    paused = true;

    menu.add_item("Inicio");
    menu.add_subitem("Facil");
    menu.add_subitem("Normal");
    menu.add_item("Tempos");




    difficulty = 1;
  }
  ~Game() {}

  void init() {
    start_time = millis();

    player.set_position(Vector2D(29,2));

    ITEMS.push_back(std::make_unique<Item>(Vector2D(25,10), "KEY", CRGB::Yellow));
    ITEMS.push_back(std::make_unique<Item>(Vector2D(33,9), "KEY", CRGB::Yellow));
    ITEMS.push_back(std::make_unique<Item>(Vector2D(2,27), "KEY", CRGB::Yellow));
    ITEMS.push_back(std::make_unique<Item>(Vector2D(2,28), "KEY", CRGB::Yellow));
    ITEMS.push_back(std::make_unique<Item>(Vector2D(9,25), "KEY", CRGB::Yellow));
    ITEMS.push_back(std::make_unique<Item>(Vector2D(40,22), "KEY", CRGB::Yellow));
  
    // Add Enemies
      //  First Room
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(24,7), Vector2D(1,0), 1000/difficulty));
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(24,9), Vector2D(1,0), 1000/difficulty));
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(24,11), Vector2D(1,0), 1000/difficulty));
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(34,8), Vector2D(-1,0), 1000/difficulty));
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(34,10), Vector2D(-1,0), 1000/difficulty));

    //  Second Room
    ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(14,12), Vector2D(0,1), 5000/difficulty));
    ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(16,12), Vector2D(0,1), 5000/difficulty));
    ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(15,27), Vector2D(0,-1), 5000/difficulty));

    // Third Room
    ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(1,20), Vector2D(1,0), 5000/difficulty));
    ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(3,31), Vector2D(0,-1), 5000/difficulty));

    // Fourth Room
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(7,24), Vector2D(0,-1), 1000/difficulty));
    ENEMIES.push_back(std::make_unique<Enemy_SidetoSide>(Vector2D(11,24), Vector2D(0,1), 1000/difficulty));

    // // Final Room
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(18,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(20,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(22,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(24,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(26,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(28,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(30,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(32,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(34,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(36,17), Vector2D(0,1), 2000));
    // ENEMIES.push_back(std::make_unique<Cannon>(Vector2D(38,17), Vector2D(0,1), 2000));

    // // Goal
    goal.set_color(CRGB::Green);
    goal.set_type("GOAL");
    goal.set_position(Vector2D(29,33));
    goal.is_alive = true;
  }

  void reset() {
    ITEMS.clear();
    ENEMIES.clear();
    player.reset();

    won = false;

    // Close doors
    for (int i = 0; i < TILEGRID_LENGHT; i++) 
      for (int j = 0; j < TILEGRID_HEIGHT; j++)
        if(TILEGRID[j][i] == OPEN_DOOR_TILE)
          TILEGRID[j][i] = DOOR_TILE;

    init();
  }

  void render() {
    fill(CRGB::Black);
    write_buffer();
    FastLED.show();
    FastLED.delay(50);
  }

  void event_handler() {
    for(auto& event: events.get()) {
      if(paused) {
        if (event == K_UP)
          menu.move(Vector2D(0,-1));
        else if (event == K_DOWN)
          menu.move(Vector2D(0,1));
        else if (event == K_LEFT)
          menu.move(Vector2D(-1,0));
        else if (event == K_RIGHT)
          menu.move(Vector2D(1,0));
        else if (event == K_r) {
          if (menu.get_item() == "Inicio" || menu.get_item() == "Tempos") {
            menu.move(Vector2D(1,0));
          } 
          else if (menu.get_item() == "Facil") {
            paused = false;
            difficulty = 1;
            reset();
          }
          else if (menu.get_item() == "Normal") {
            paused = false;
            difficulty = 2;
            reset();
          }
        }
      }
      else {
        if (event == K_r) 
          reset();
        else if (event == K_p)
          paused = true;
        player.process_input(event);
      }
    }
  }

  void add_event(int event) {
    events.add(event);
  }

  void process() {
    event_handler();
    if (paused) {
      menu.render();
      delay(200);
    }
    else {
      render();
      player.process();
      camera.set_position(player.get_position());
      camera.process();

      for(auto& enemy : ENEMIES)
        enemy->process();

      if (goal.is_colliding(player)) {
          paused = true;
          menu.add_subitem(String((millis() - start_time)/1000) + "s");
      }


      ITEMS.erase(std::remove_if(
        ITEMS.begin(), 
        ITEMS.end(), [](auto const& item) { 
          return !item->is_alive;}), 
        ITEMS.end());

      ENEMIES.erase(std::remove_if(
        ENEMIES.begin(), 
        ENEMIES.end(), [](auto const& enemy) { 
          return !enemy->is_alive;}), 
        ENEMIES.end());
    }
    
  }

private:
  Camera camera;
  Event events;
  Player player;
  Menu menu;
  Item goal;

  bool paused;
  int difficulty;
  bool won;

  unsigned long start_time;


  void write_buffer() {
    // Tiles
    for (int i =0; i < camera.get_projection().x; i++) {
      for (int j =0; j < camera.get_projection().y; j++) {
        int tile = TILEGRID[j + camera.get_viewposition().y][i + camera.get_viewposition().x];
        if(tile == 1) // Wall
          led(i, j, CRGB::White);
        else if (tile == 2) // Door
          led(i, j, CRGB(102,57,49));
      }
    }

    // ITEMS
    for(auto& item : ITEMS)
      if(in_view(*item))
        led(item->get_position() - camera.get_viewposition(), item->get_color());

    // GOAL
    if(in_view(goal)) {
      led(goal.get_position() - camera.get_viewposition(), goal.get_color());
    }

    // PLAYER
    if(in_view(player))
      led(player.get_position() - camera.get_viewposition(), player.get_color());

    // ENEMIES
    for(auto& enemy : ENEMIES)
      if(in_view(*enemy))
        led(enemy->get_position() - camera.get_viewposition(), enemy->get_color());


  }

  bool in_view(const Entity& entity) {
    if (entity.get_position().x >= camera.get_viewposition().x &&
        entity.get_position().x < camera.get_viewposition().x + camera.get_projection().x &&
        entity.get_position().y >= camera.get_viewposition().y &&
        entity.get_position().y < camera.get_viewposition().y + camera.get_projection().y)
      return true;
    else
      return false;
  }
};

Game game;

void setup_wifi() {
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      // ... and resubscribe
      client.publish("$INF351/test", "MQTT Server is Connected");
      client.subscribe("$INF351/#");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String str_topic = String(topic);
  if (str_topic == "$INF351/EVENT")
      game.add_event(payload[0]); // UP
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(50);

    matrix->begin();
    matrix->setTextWrap(false);
    // matrix->setBrightness(90);
    matrix->setTextSize(1);
    matrix->setFont(&Picopixel);

    // sanity check delay - allows reprogramming if accidently blowing power w/leds
    delay(2000);

    // game.init();

}

// void read_lcd_input() {
//   int read = analogRead(A0);

//   for (int new_key = 0;;new_key++)
//     if (read < lcd_keys[new_key].limit)
//       game.add_event(lcd_keys[new_key].key);

// }

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  // read_lcd_input();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
 
  }

  game.process();
}