import PageTemplate from '../Template/PageTemplate';
import background from './LoginDesign.svg';
import './LoginPage.css'
import GoogleBtn from '../../components/GoogleBtn/GoogleBtn';


const LoginPage = () => {
  return (
    <PageTemplate>
      <div className="loginPageButton" data-testid="login-page">
        <GoogleBtn />
      </div>
      <img src={background} alt="ppt background" className="loginPageBackground" />
    </PageTemplate>
  );
}

export default LoginPage