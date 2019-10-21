//
// Created by cybergnome on 10/22/19.
//

#ifndef CLIENT_LOGIN_H
#define CLIENT_LOGIN_H


#include <QMainWindow>

namespace Ui {
    class LoginWindow;
}

class LoginWindow : public QMainWindow
{
Q_OBJECT

public:
    explicit LoginWindow(QWidget *parent = 0);
    ~LoginWindow();

private:
    Ui::LoginWindow *ui;
};


#endif //CLIENT_LOGIN_H
