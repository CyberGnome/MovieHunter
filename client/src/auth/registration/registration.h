//
// Created by cybergnome on 10/22/19.
//

#ifndef CLIENT_REGISTRATION_H
#define CLIENT_REGISTRATION_H


#include <QMainWindow>

namespace Ui {
    class RegistrationWindow;
}

class RegistrationWindow : public QMainWindow
{
Q_OBJECT

public:
    explicit RegistrationWindow(QWidget *parent = nullptr);
    ~RegistrationWindow();

private:
    Ui::RegistrationWindow *ui;
};


#endif //CLIENT_REGISTRATION_H
