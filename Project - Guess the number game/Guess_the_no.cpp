#include <iostream>
#include <fstream>
#include <ctime>
#include <unistd.h>
using namespace std;

void character_by_character_display(string messages)
{
    for (char c : messages)
    {
        cout << c << flush;
        usleep(100000); // pause for 100000 microseconds
    }
}

// Class object
class RandomNumber
{
private:
    string msg = "\n\nDestroying the Random Number Generated\nExitting....\n";
    int number;

public:
    // Constructor
    RandomNumber()
    {
        srand(time(0));
        number = rand() % 100 + 1;
    }
    // Destructor
    ~RandomNumber()
    {
        character_by_character_display(msg);
    }
    int getNumber()
    {
        return number;
    }
};

// Inheritance
class GuessGame : public RandomNumber
{
private:
    int guess;

public:
    // Polymorphism
    virtual void play()
    {
        cout << "Guess a number between 1 and 100 : ";
        cin >> guess;
        while (guess != getNumber())
        {
            if (guess < getNumber())
            {
                cout << "Too low. Guess Again : ";
                cin >> guess;
            }
            else
            {
                cout << "Too high. Guess Again : ";
                cin >> guess;
            }
        }
        cout << "\nCongratulations! You guessed the correct number!" << endl;
    }
};

// Template
template <typename T>
void handleFile(T &game)
{
    string fileName;
    cout << "\nEnter a file name : ";
    cin >> fileName;
    fileName += ".txt";
    ofstream outFile(fileName);
    outFile << game.getNumber();
    outFile.close();
}

int main()
{
    GuessGame game;
    int ch;
    string mg = "Welcome to Guess the Number Game.\n\n";
    string message = "\nThanks for playing !!!";
    character_by_character_display(mg);
    do
    {
        cout << "\nWant to play the game ?\n" << endl;
        cout << "1. Play Game" << endl;
        cout << "2. Exit\n" << endl;
        cout << "Enter choice : ";
        cin >> ch;
        switch (ch)
        {
        case 1:
        {
            game.play();
            // File handling
            handleFile(game);
            game = GuessGame();
            break;
        }
        case 2:
        {
            break;
        }
        default:
        {
            cout << "\nInvalid choice !!!\n\nChoose options between 1 and 2" << endl;
        }
        }
    } while (ch != 2);
    character_by_character_display(message);
    return 0;
}