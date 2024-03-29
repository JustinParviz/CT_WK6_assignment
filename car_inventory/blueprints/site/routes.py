from flask import Blueprint, flash, redirect, render_template, request 


#internal import 
from car_inventory.models import Car, Customer, Order, db 
from car_inventory.forms import CarForm


#need to instantiate our Blueprint class

site = Blueprint('site', __name__, template_folder='site_templates')


#use site object to create our routes
@site.route('/')
def shop():

    #we need to query our database to grab all of our products to display
    allprods = Car.query.all() #the same as SELECT * FROM products, list of objects 
    allcustomers = Customer.query.all()
    allorders = Order.query.all()
    
    #making our dictionary for our shop stats/info

    shop_stats = {
        'products' : len(allprods), #this is how many total products we have
        'sales' : sum([order.order_total for order in allorders]),  #[ 27.99, 83.25, 50.99 ] sum them bad boys up
        'customers' : len(allcustomers)
    }
    
    
    our_class = "Justin's inventory is the best "
                            #whats on left side is html, right side is whats in our route
    return render_template('shop.html', shop=allprods, coolmessage = our_class, stats=shop_stats) #looking inside our template_folder (site_templates) to find our shop.html file



@site.route('/shop/create', methods= ['GET', 'POST'])
def create():

    #instantiate our productform

    createform = CarForm()

    if request.method == 'POST' and createform.validate_on_submit():
        #grab our data from our form
        make = createform.make.data
        model = createform.model.data
        year = createform.year.data
        color = createform.color.data
        horsepower = createform.horsepower.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data 

        #instantiate that class as an object passing in our arguments to replace our parameters 
        
        car = Car(make, model, year, color, price, quantity, horsepower, image, description)
        print(car)

        db.session.add(car) #adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have successfully added car {make} {model}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        make = createform.make.data
        model = createform.model.data
        year = createform.year.data
        color = createform.color.data
        horsepower = createform.horsepower.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data 

        print(make, model, year, color, "horsepower", horsepower, "image", image, "description", description, price, quantity)
        return redirect('/shop/create')
    

    return render_template('create.html', form=createform )


@site.route('/shop/update/<id>', methods=['GET', 'POST']) #<parameter> this is how pass parameters to our routes 
def update(id):

    #lets grab our specific product we want to update
    car = Car.query.get(id) #this should only ever bring back 1 item/object
    
    updateform = CarForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        car.make = updateform.make.data 
        car.model = updateform.model.data
        car.year = updateform.year.data
        car.color = updateform.color.data
        car.horsepower = updateform.horsepower.data
        car.image = car.image = car.set_image(updateform.image.data, updateform.name.data)
        car.description = updateform.description.data 
        car.price = updateform.price.data 
        car.quantity = updateform.quantity.data 

        #commit our changes
        db.session.commit()

        flash(f"You have successfully updated car {car.make} {car.model}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/')
    
    return render_template('update.html', form=updateform, car=car )


@site.route('/shop/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    car = Car.query.get(id)

    db.session.delete(car)
    db.session.commit()

    return redirect('/')