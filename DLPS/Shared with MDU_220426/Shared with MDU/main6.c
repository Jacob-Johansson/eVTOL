#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_multifit_nlinear.h>

#define N      5    /* number of position differences */
#define SPEED_OF_LIGHT  300000000

struct data {
  size_t n;
  double * t;
  double * y;
  double * positions
};

typedef struct beacon_pos 
{
    double x;
    double y;
    double z;
} beacon_pos;

typedef struct ddist 
{
    double a_b;
    double a_c;
    double a_d;
    
} ddist;

int
expb_f (const gsl_vector * x, void *data,
        gsl_vector * f)
{
  size_t n = ((struct data *)data)->n;
  double *t = ((struct data *)data)->t;
  double *y = ((struct data *)data)->y;
  double *positions = ((struct data *)data)->positions;
  
  double xpos = gsl_vector_get (x, 0);
  double ypos = gsl_vector_get (x, 1);
  double zpos = gsl_vector_get (x, 2);
  //Beacon1
  double pos1X = positions[0];
  double pos1Y = positions[1];
  double pos1Z = positions[2];
  /*/Beacon2
  double pos2X = positions[3];
  double pos2Y = positions[4];
  double pos2Z = positions[5];
  //Beacon3
  double pos3X = positions[6];
  double pos3Y = positions[7];
  double pos3Z = positions[8];
  //Beacon4
  double pos4X = positions[9];
  double pos4Y = positions[10];
  double pos4Z = positions[11];
  //Beacon5
  double pos5X = positions[12];
  double pos5Y = positions[13];
  double pos5Z = positions[14];*/
    
  double dist_bi = 0;
  double dist_b1 = sqrt(pow((pos1X-xpos),2)+pow((pos1Y-ypos),2)+pow((pos1Z-pow(zpos,2)),2));
  double result;
  double punishment;
  int ind1, ind2, ind3;

  size_t i;

  for (i = 0; i < n; i++)
    {
      ind1 = i*3+(3);
      ind2 = i*3+(4);
      ind3 = i*3+(5);
      dist_bi = sqrt(pow((positions[ind1]-xpos),2)+pow((positions[ind2]-ypos),2)+pow((positions[ind3]-pow(zpos,2)),2));
      if (zpos<0)
        {
          punishment = zpos*zpos*100;
        }
      else
        {
          punishment = 0;
        }
      result = (dist_b1-dist_bi)-y[i]+punishment;
      //fprintf(stderr," \nx=%f, y=%f, z=%f: Dist to B1: %f, Dist to B%i: %f, Diff: %f, Diff to fit: %f",xpos,ypos,zpos,dist_b1,i+2,dist_bi,dist_b1-dist_bi,y[i]);
      //fprintf(stderr, "\nB%i_X: %f, Y: %f , Z: %f",i+2,positions[ind1],positions[ind2],positions[ind3]);
      //fprintf(stderr, "\nResult %i = %f. Indexes: %i ,%i, %i\n",i, result, ind1, ind2, ind3);
      gsl_vector_set (f, i, result);
    }

  return GSL_SUCCESS;
}


void
callback(const size_t iter, void *params,
         const gsl_multifit_nlinear_workspace *w)
{
  gsl_vector *f = gsl_multifit_nlinear_residual(w);
  gsl_vector *x = gsl_multifit_nlinear_position(w);
  double rcond;

  /* compute reciprocal condition number of J(x) */
  gsl_multifit_nlinear_rcond(&rcond, w);
  
  fprintf(stderr, "iter %2zu: X = %.4f, Y = %.4f, Z = %.4f, cond(J) = %8.4f, |f(x)| = %.4f\n",
          iter,
          gsl_vector_get(x, 0),
          gsl_vector_get(x, 1),
          gsl_vector_get(x, 2),
          1.0 / rcond,
          gsl_blas_dnrm2(f));
           
}


double * calc_pos (const double * inputvector)//(ddist diff, beacon_pos coordA,beacon_pos coordB,beacon_pos coordC, beacon_pos coordD)
{

  //fprintf(stderr,"Inputs 1-5 are: %f, %f, %f, %f ,%f",inputvector[0],inputvector[1],inputvector[2],inputvector[3],inputvector[4]); 
  const gsl_multifit_nlinear_type *T = gsl_multifit_nlinear_trust;
  gsl_multifit_nlinear_workspace *w;
  gsl_multifit_nlinear_fdf fdf;
  gsl_multifit_nlinear_parameters fdf_params =
    gsl_multifit_nlinear_default_parameters();
  const size_t n = N;
  const size_t p = 3;
  

  gsl_vector *f;
  gsl_matrix *J;
  gsl_matrix *covar = gsl_matrix_alloc (p, p);
  double t[N], y[N], weights[N], positions[19];
  //Beacon 1 XYZ:
  positions[0] = inputvector[3+2];
  positions[1] = inputvector[4+2];
  positions[2] = inputvector[5+2];
  //Beacon 2 XYZ:
  positions[3] = inputvector[6+2];
  positions[4] = inputvector[7+2];
  positions[5] = inputvector[8+2];
  //Beacon 3 XYZ:
  positions[6] = inputvector[9+2];
  positions[7] = inputvector[10+2];
  positions[8] = inputvector[11+2];
  //Beacon 4 XYZ:
  positions[9] = inputvector[12+2];
  positions[10] = inputvector[13+2];
  positions[11] = inputvector[14+2];
  //Beacon 5 XYZ:
  positions[12] = inputvector[15+2];
  positions[13] = inputvector[16+2];
  positions[14] = inputvector[17+2];
  //Beacon 6 XYZ:
  positions[15] = inputvector[18+2];
  positions[16] = inputvector[19+2];
  positions[17] = inputvector[20+2];
  
  struct data d = { n, t, y , positions};
  double x_init[3] = {5,5,5}; /* starting values */
  gsl_vector_view x = gsl_vector_view_array (x_init, p);
  gsl_vector_view wts = gsl_vector_view_array(weights, n);
  gsl_rng * r;
  double chisq, chisq0;
  int status, info;
  size_t i;

  const double xtol = 1e-8;
  const double gtol = 1e-8;
  const double ftol = 0.0;

  gsl_rng_env_setup();
  r = gsl_rng_alloc(gsl_rng_default);

  /* define the function to be minimized */
  fdf.f = expb_f;
  fdf.df = NULL;   /* set to NULL for finite-difference Jacobian */
  fdf.fvv = NULL;     /* not using geodesic acceleration */
  fdf.n = n;
  fdf.p = p;
  fdf.params = &d;

  /* this is the data to be fitted */

  y[0] = inputvector[0];//5.20999e-9;
  y[1] = inputvector[1];//-1.6900e-9;
  y[2] = inputvector[2];//3.373e-8;
  y[3] = inputvector[3];//3.373e-8;
  y[4] = inputvector[4];//3.373e-8;
  
  weights[0] = 1.0;
  weights[1] = 1.0;
  weights[2] = 1.0;
  weights[3] = 1.0;
  weights[4] = 1.0;

  /* allocate workspace with default parameters */
  w = gsl_multifit_nlinear_alloc (T, &fdf_params, n, p);

  /* initialize solver with starting point and weights */
  gsl_multifit_nlinear_winit (&x.vector, &wts.vector, &fdf, w);

  /* compute initial cost function */
  f = gsl_multifit_nlinear_residual(w);
  gsl_blas_ddot(f, f, &chisq0);

  /* solve the system with a maximum of 100 iterations */
  status = gsl_multifit_nlinear_driver(100, xtol, gtol, ftol,
                                       NULL, NULL, &info, w);

  /* compute covariance of best fit parameters */
  J = gsl_multifit_nlinear_jac(w);
  gsl_multifit_nlinear_covar (J, 0.0, covar);

  /* compute final cost */
  gsl_blas_ddot(f, f, &chisq);

#define FIT(i) gsl_vector_get(w->x, i)
#define ERR(i) sqrt(gsl_matrix_get(covar,i,i))
/* 
  fprintf(stderr, "summary from method '%s/%s'\n",
          gsl_multifit_nlinear_name(w),
          gsl_multifit_nlinear_trs_name(w));
  fprintf(stderr, "number of iterations: %zu\n",
          gsl_multifit_nlinear_niter(w));
  fprintf(stderr, "function evaluations: %zu\n", fdf.nevalf);
  fprintf(stderr, "Jacobian evaluations: %zu\n", fdf.nevaldf);
  fprintf(stderr, "reason for stopping: %s\n",
          (info == 1) ? "small step size" : "small gradient");
  fprintf(stderr, "initial |f(x)| = %f\n", sqrt(chisq0));
  fprintf(stderr, "final   |f(x)| = %f\n", sqrt(chisq));

  {
    double dof = n - p;
    double c = GSL_MAX_DBL(1, sqrt(chisq / dof));

    fprintf(stderr, "chisq/dof = %g\n", chisq / dof);

    fprintf (stderr, "x      = %.5f +/- %.5f\n", FIT(0), c*ERR(0));
    fprintf (stderr, "y      = %.5f +/- %.5f\n", FIT(1), c*ERR(1));
    fprintf (stderr, "z      = %.5f +/- %.5f\n", FIT(2), c*ERR(2));
  }
 */
  //fprintf (stderr, "statusL = %s\n", gsl_strerror (status));
  
  //gsl_multifit_nlinear_free (w);
  gsl_matrix_free (covar);
  gsl_rng_free (r);
  static double mupp[5];
  mupp[0] = FIT(0);
  mupp[1] = FIT(1);
  mupp[2] = pow(FIT(2),2);
  mupp[3] = sqrt(chisq);
  mupp[4] = 1;
  if (status)
  {
    mupp[4] = -1;
  }
  gsl_multifit_nlinear_free (w);
  return mupp;
}

double *  main(void)
{
    ddist kalle = {1,2,3};
    beacon_pos coordA = {0,0,0};
    beacon_pos coordB = {14,0,0};
    beacon_pos coordC = {0,14,0};
    beacon_pos coordD = {14,14,10};
    kalle.a_b = 8.610e-9*SPEED_OF_LIGHT;
    kalle.a_c =-1.640e-9*SPEED_OF_LIGHT;
    kalle.a_d = 3.751e-8*SPEED_OF_LIGHT;
        
    //while(1)
                
    static double somepos_var[3];
    somepos_var[0] = 32141.432;
    somepos_var[1] = 34443.324;
    somepos_var[2] = 12354.3424;
    //somepos_var   = calc_pos(kalle, coordA, coordB, coordC, coordD);
        

    static int skitvariabel[3] = {11,22,33};
    return somepos_var;
}
