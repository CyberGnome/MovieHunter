#include <QApplication>

#include "moviehunter.h"
#include "../auth/login.h"


int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MovieHunter mhW;
    mhW.show();

    LoginWindow lW(&mhW);
    lW.show();

    return app.exec();
}
